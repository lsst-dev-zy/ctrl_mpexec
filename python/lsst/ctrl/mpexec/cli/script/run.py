# This file is part of ctrl_mpexec.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from types import SimpleNamespace

from lsst.daf.butler.cli.cliLog import CliLog
from ... import CmdLineFwk, TaskFactory

_log = logging.getLogger(__name__.partition(".")[2])


def run(do_raise,
        graph_fixup,
        init_only,
        log_level,
        no_versions,
        processes,
        profile,
        qgraphObj,
        register_dataset_types,
        skip_init_writes,
        timeout,
        butler_config,
        input,
        output,
        output_run,
        extend_run,
        replace_run,
        prune_replaced,
        data_query,
        skip_existing,
        debug,
        fail_fast,
        **kwargs):
    """Implements the command line interface `pipetask run` subcommand, should
    only be called by command line tools and unit test code that test this
    function.

    Parameters
    ----------
    do_raise : `bool`
        Raise an exception in the case of an error.
    graph_fixup : `str`
        The name of the class or factory method which makes an instance used
        for execution graph fixup.
    init_only : `bool`
        If true, do not actually run; just register dataset types and/or save
        init outputs.
    log_level : `list` of `tuple`
        per-component logging levels, each item in the list is a tuple
        (component, level), `component` is a logger name or an empty string
        or `None` for root logger, `level` is a logging level name, one of
        CRITICAL, ERROR, WARNING, INFO, DEBUG (case insensitive).
    no_versions : `bool`
        If true, do not save or check package versions.
    processes : `int`
        The number of processes to use.
    profile : `str`
        File name to dump cProfile information to.
    qgraphObj : `lsst.pipe.base.QuantumGraph`
        A QuantumGraph generated by a previous subcommand.
    register_dataset_types : `bool`
        If true, register DatasetTypes that do not already exist in the Registry.
    skip_init_writes : `bool`
        If true, do not write collection-wide 'init output' datasets (e.g.
        schemas).
    timeout : `int`
        Timeout for multiprocessing; maximum wall time (sec).
    butler_config : `str`, `dict`, or `lsst.daf.butler.Config`
        If `str`, `butler_config` is the path location of the gen3
        butler/registry config file. If `dict`, `butler_config` is key value
        pairs used to init or update the `lsst.daf.butler.Config` instance. If
        `Config`, it is the object used to configure a Butler.
    input : `str`
        Comma-separated names of the input collection(s). Entries may include a
        colon (:), the first string is a dataset type name that restricts the
        search in that collection.
    output : `str`
        Name of the output CHAINED collection. This may either be an existing
        CHAINED collection to use as both input and output (if `input` is
        `None`), or a new CHAINED collection created to include all inputs
        (if `input` is not `None`). In both cases, the collection's children
        will start with an output RUN collection that directly holds all new
        datasets (see `output_run`).
    output_run : `str`
        Name of the new output RUN collection. If not provided then `output`
        must be provided and a new RUN collection will be created by appending
        a timestamp to the value passed with `output`. If this collection
        already exists then `extend_run` must be passed.
    extend_run : `bool`
        Instead of creating a new RUN collection, insert datasets into either
        the one given by `output_run` (if provided) or the first child
        collection of `output` (which must be of type RUN).
    replace_run : `bool`
        Before creating a new RUN collection in an existing CHAINED collection,
        remove the first child collection (which must be of type RUN). This can
        be used to repeatedly write to the same (parent) collection during
        development, but it does not delete the datasets associated with the
        replaced run unless `prune-replaced` is also True. Requires `output`,
        and `extend_run` must be `None`.
    prune_replaced : "unstore", "purge", or `None`.
        If not `None`, delete the datasets in the collection replaced by
        `replace_run`, either just from the datastore ("unstore") or by
        removing them and the RUN completely ("purge"). Requires `replace_run`.
    data_query : `str`
        User query selection expression.
    skip_existing : `bool`
        If all Quantum outputs already exist in the output RUN collection then
        that Quantum will be excluded from the QuantumGraph. Requires the 'run`
        command's `--extend-run` flag to be set.
    debug : `bool`
        If true, enable debugging output using lsstDebug facility (imports
        debug.py).
    fail_fast : `bool`
        If true then stop processing at first error, otherwise process as many
        tasks as possible.
    kwargs : `dict` [`str`, `str`]
        Ignored; click commands may accept options for more than one script
        function and pass all the option kwargs to each of the script functions
        which ingore these unused kwargs.
    """

    if log_level is not None:
        CliLog.setLogLevels(log_level)

    args = SimpleNamespace(do_raise=do_raise,
                           graph_fixup=graph_fixup,
                           init_only=init_only,
                           no_versions=no_versions,
                           processes=processes,
                           profile=profile,
                           skip_init_writes=skip_init_writes,
                           timeout=timeout,
                           register_dataset_types=register_dataset_types,
                           butler_config=butler_config,
                           input=input,
                           output=output,
                           output_run=output_run,
                           extend_run=extend_run,
                           replace_run=replace_run,
                           prune_replaced=prune_replaced,
                           data_query=data_query,
                           skip_existing=skip_existing,
                           enableLsstDebug=debug,
                           fail_fast=fail_fast)

    f = CmdLineFwk()
    taskFactory = TaskFactory()
    f.runPipeline(qgraphObj, taskFactory, args)