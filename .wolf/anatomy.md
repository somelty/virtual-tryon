# anatomy.md

> Auto-maintained by OpenWolf. Last scanned: 2026-05-07T13:25:11.899Z
> Files: 547 tracked | Anatomy hits: 0 | Misses: 0

## ./

- `.gitignore` — Git ignore rules (~6 tok)
- `安装扩展包.txt` (~116 tok)
- `app_old.py` — Original app.py backup (~1128 tok)
- `app.py` — load_user, create_app (~338 tok)
- `CLAUDE.md` — OpenWolf (~682 tok)
- `config.py` — Declares Config (~193 tok)
- `docs/superpowers/specs/2026-05-07-virtual-tryon-multi-user-design.md` (~332 tok)
- `model.py` — FashionCNN: forward (~478 tok)
- `show.py` (~518 tok)
- `train.py` (~1309 tok)

## .claude/

- `settings.json` (~441 tok)

## .claude/rules/

- `openwolf.md` (~313 tok)

## blueprints/

- `__init__.py` (~0 tok)
- `auth.py` — register, login, logout, verify_email (~1346 tok)
- `main.py` — index, upload_photo, set_active_photo, delete_photo (~660 tok)
- `tryon.py` — try_on (~456 tok)
- `wardrobe.py` — index, upload, edit, delete (~969 tok)

## data/FashionMNIST/raw/

- `t10k-labels-idx1-ubyte` (~2669 tok)
- `train-labels-idx1-ubyte` (~16003 tok)

## docs/superpowers/plans/

- `2026-05-07-virtual-tryon-multi-user.md` — 虚拟试衣多用户系统 — 实施计划 (~19615 tok)

## docs/superpowers/specs/

- `2026-05-07-virtual-tryon-multi-user-design.md` — 虚拟试衣多用户系统 — 设计文档 (~970 tok)

## engines/

- `__init__.py` — get_engine (~95 tok)
- `base.py` — TryOnEngine: composite (~79 tok)
- `mediapipe.py` — MediaPipeEngine: pose, midpoint, composite (~1508 tok)
- `simple.py` — SimpleEngine: composite (~392 tok)

## models/

- `__init__.py` (~45 tok)
- `clothing.py` — Clothing: display_category (~161 tok)
- `photo.py` — Photo: set_active (~145 tok)
- `user.py` — User(UserMixin): set_password, check_password, get_active_photo, generate_verification_token + 1 more (~518 tok)

## templates/

- `base.html` — {% block title %}FitAI{% endblock %} · 智能试衣 (~3316 tok)
- `index.html` — FitAI · 智能试衣 (~8451 tok)
- `login.html` — 登录 · 智能试衣 (~202 tok)
- `register.html` — 注册 · 智能试衣 (~271 tok)
- `reset_password.html` — 重置密码 · 智能试衣 (~295 tok)
- `wardrobe.html` — 衣物库 · FitAI (~1462 tok)

## tests/

- `__init__.py` (~0 tok)
- `conftest.py` — app, client, runner, logged_in_user (~247 tok)
- `test_auth.py` — TestRegister: test_register_page_loads, test_register_success, test_register_duplicate_username, tes (~1588 tok)
- `test_models.py` — TestUserModel: test_create_user, test_username_unique, test_email_unique, test_create_photo + 5 more (~1630 tok)
- `test_photo.py` — TestPhotoUpload: test_upload_photo, test_set_active_photo, test_cannot_access_other_user_photo, test (~785 tok)
- `test_tryon.py` — TestTryOn: test_tryon_endpoint, test_tryon_no_active_photo, test_tryon_other_user_clothing (~681 tok)
- `test_wardrobe.py` — TestWardrobe: test_wardrobe_page, test_upload_clothing, test_edit_category, test_delete_clothing + 1 (~831 tok)

## utils/

- `__init__.py` (~0 tok)
- `email.py` — send_verification_email, send_reset_email (~132 tok)
- `image.py` — allowed_file, save_upload, validate_image (~286 tok)

## venv/

- `.gitignore` — Git ignore rules (~19 tok)
- `pyvenv.cfg` (~54 tok)

## venv/Lib/site-packages/

- `distutils-precedence.pth` (~41 tok)
- `isympy.py` — main (~3202 tok)
- `pylab.py` (~32 tok)
- `six.py` — Utilities for writing code that runs on Python 2 and 3 (~9916 tok)
- `typing_extensions.py` — _Sentinel: final, done, done, disjoint_base + 1 more (~45837 tok)

## venv/Lib/site-packages/_distutils_hack/

- `__init__.py` — don't import any costly modules (~1930 tok)
- `override.py` (~13 tok)

## venv/Lib/site-packages/blinker-1.9.0.dist-info/

- `INSTALLER` (~2 tok)
- `LICENSE.txt` (~264 tok)
- `METADATA` (~436 tok)
- `RECORD` (~222 tok)
- `WHEEL` (~22 tok)

## venv/Lib/site-packages/blinker/

- `__init__.py` (~91 tok)
- `_utilities.py` — Symbol: make_id, make_ref (~479 tok)
- `base.py` — Signal: receiver_connected, receiver_disconnected, connect, connect_via + 7 more (~5467 tok)
- `py.typed` (~0 tok)

## venv/Lib/site-packages/click-8.3.3.dist-info/

- `INSTALLER` (~2 tok)
- `METADATA` — Declares toolkit (~699 tok)
- `RECORD` (~675 tok)
- `WHEEL` (~22 tok)

## venv/Lib/site-packages/click-8.3.3.dist-info/licenses/

- `LICENSE.txt` (~369 tok)

## venv/Lib/site-packages/click/

- `__init__.py` (~1294 tok)
- `_compat.py` — URL configuration (~5341 tok)
- `_termui_impl.py` — ProgressBar: render_finish, pct, time_per_iteration, eta + 11 more (~8019 tok)
- `_textwrap.py` — TextWrapper: extra_indent, indent_only (~400 tok)
- `_utils.py` — Declares import (~270 tok)
- `_winconsole.py` — This module is based on the excellent work by Adam Bartoš who (~2419 tok)
- `core.py` — ParameterSource: batch, augment_usage_errors, iter_params_for_processing, sort_key (~38423 tok)
- `decorators.py` — to: pass_context, new_func, pass_obj, new_func + 24 more (~5275 tok)
- `exceptions.py` — ClickException: format_message, show, show, format_message + 4 more (~2844 tok)
- `formatting.py` — Can force a width.  This is used by the test system (~2780 tok)
- `globals.py` — get_current_context, get_current_context, get_current_context, push_context + 2 more (~550 tok)
- `parser.py` — _Option: takes_value, process, process, add_option + 2 more (~5432 tok)
- `py.typed` (~0 tok)
- `shell_completion.py` — CompletionItem: shell_complete, func_name, source_vars, source + 9 more (~5999 tok)
- `termui.py` — hidden_prompt_func, prompt, prompt_func, confirm + 4 more (~8982 tok)
- `testing.py` — EchoingStdin: read, read1, readline, readlines + 13 more (~6490 tok)
- `types.py` — ParamType: to_info_dict, get_metavar, get_missing_message, convert + 14 more (~11408 tok)
- `utils.py` — URL configuration (~5795 tok)

## venv/Lib/site-packages/colorama-0.4.6.dist-info/

- `INSTALLER` (~2 tok)
- `METADATA` — multiple: all (~4574 tok)
- `RECORD` (~580 tok)
- `WHEEL` (~28 tok)

## venv/Lib/site-packages/colorama-0.4.6.dist-info/licenses/

- `LICENSE.txt` (~373 tok)

## venv/Lib/site-packages/colorama/

- `__init__.py` (~76 tok)
- `ansi.py` — AnsiCodes: code_to_chars, set_title, clear_screen, clear_line + 5 more (~721 tok)
- `ansitowin32.py` — StreamWrapper: write, isatty, closed, should_wrap + 10 more (~3180 tok)
- `initialise.py` — reset_all, init, deinit, just_fix_windows_console + 3 more (~950 tok)
- `win32.py` — from winbase.h (~1766 tok)
- `winterm.py` — WinColor: get_osfhandle, get_attrs, set_attrs, reset_all + 11 more (~2039 tok)

## venv/Lib/site-packages/colorama/tests/

- `__init__.py` (~22 tok)
- `ansi_test.py` — Test file (~812 tok)
- `ansitowin32_test.py` — Tests: closed_shouldnt_raise_on_closed_stream, closed_shouldnt_raise_on_detached_stream, reset_all_shouldnt_raise_on_closed_orig_stdout, wrap_shoul... (~3051 tok)
- `initialise_test.py` — Test file (~1926 tok)
- `isatty_test.py` — Tests: TTY, nonTTY, withPycharm, withPycharmTTYOverride + 3 more (~534 tok)
- `utils.py` — StreamTTY: isatty, isatty, osname, replace_by + 2 more (~309 tok)
- `winterm_test.py` — Test file (~1060 tok)

## venv/Lib/site-packages/contourpy-1.3.3.dist-info/

- `INSTALLER` (~2 tok)
- `LICENSE` — Project license (~417 tok)
- `METADATA` (~1457 tok)
- `RECORD` (~809 tok)
- `WHEEL` (~23 tok)

## venv/Lib/site-packages/contourpy/

- `__init__.py` — name: contour_generator (~3443 tok)
- `_contourpy.cp313-win_amd64.lib` (~552 tok)
- `_contourpy.cp313-win_amd64.pyd` (~121301 tok)
- `_contourpy.pyi` — Input numpy array types, the same as in common.h (~1953 tok)
- `_version.py` (~7 tok)
- `array.py` — codes_from_offsets, codes_from_offsets_and_points, codes_from_points, concat_codes + 16 more (~2640 tok)
- `chunk.py` — calc_chunk_sizes, two_factors (~964 tok)
- `convert.py` — convert_filled (~7650 tok)
- `dechunk.py` — dechunk_filled, dechunk_lines, dechunk_multi_filled, dechunk_multi_lines (~2276 tok)
- `enum_util.py` — as_fill_type, as_line_type, as_z_interp (~451 tok)
- `py.typed` (~0 tok)
- `typecheck.py` — check_code_array, check_offset_array, check_point_array, check_filled + 1 more (~3129 tok)
- `types.py` — dtypes of arrays returned by ContourPy. (~75 tok)

## venv/Lib/site-packages/contourpy/util/

- `__init__.py` (~36 tok)
- `_build_config.py` — _build_config.py.in is converted into _build_config.py during the meson build process. (~595 tok)
- `bokeh_renderer.py` — BokehRenderer: filled, grid, lines, mask + 5 more (~4050 tok)
- `bokeh_util.py` — filled_to_bokeh, lines_to_bokeh (~823 tok)
- `data.py` — simple, random (~762 tok)
- `mpl_renderer.py` — MplRenderer: filled, grid, lines, mask + 5 more (~5894 tok)
- `mpl_util.py` — filled_to_mpl_paths, lines_to_mpl_paths (~1009 tok)
- `renderer.py` — Renderer: filled, grid, lines, mask + 7 more (~1510 tok)

## venv/Lib/site-packages/cycler-0.12.1.dist-info/

- `INSTALLER` (~2 tok)
- `LICENSE` — Project license (~400 tok)
- `METADATA` (~1008 tok)
- `RECORD` (~180 tok)
- `top_level.txt` (~2 tok)
- `WHEEL` (~25 tok)

## venv/Lib/site-packages/cycler/

- `__init__.py` — Cycler: concat, keys, change_key, by_key (~4774 tok)
- `py.typed` (~0 tok)

## venv/Lib/site-packages/dateutil/

- `__init__.py` — -*- coding: utf-8 -*- (~178 tok)
- `_common.py` — Declares weekday (~267 tok)
- `_version.py` — file generated by setuptools_scm (~48 tok)
- `easter.py` — -*- coding: utf-8 -*- (~766 tok)
- `relativedelta.py` — -*- coding: utf-8 -*- (~7116 tok)
- `rrule.py` — -*- coding: utf-8 -*- (~19017 tok)
- `tzwin.py` — tzwin has moved to dateutil.tz.win (~17 tok)
- `utils.py` — -*- coding: utf-8 -*- (~562 tok)

## venv/Lib/site-packages/dateutil/parser/

- `__init__.py` — -*- coding: utf-8 -*- (~505 tok)
- `_parser.py` — -*- coding: utf-8 -*- (~16799 tok)
- `isoparser.py` — -*- coding: utf-8 -*- (~3780 tok)

## venv/Lib/site-packages/dateutil/tz/

- `__init__.py` — -*- coding: utf-8 -*- (~127 tok)
- `_common.py` — of: tzname_in_python2, adjust_encoding, enfold, replace + 10 more (~3708 tok)
- `_factories.py` — _TzSingleton: instance (~734 tok)
- `tz.py` — -*- coding: utf-8 -*- (~17959 tok)
- `win.py` — -*- coding: utf-8 -*- (~3696 tok)

## venv/Lib/site-packages/dateutil/zoneinfo/

- `__init__.py` — -*- coding: utf-8 -*- (~1683 tok)
- `rebuild.py` — rebuild (~684 tok)

## venv/Lib/site-packages/filelock-3.29.0.dist-info/

- `INSTALLER` (~2 tok)
- `METADATA` (~527 tok)
- `RECORD` (~611 tok)
- `WHEEL` (~24 tok)

## venv/Lib/site-packages/filelock-3.29.0.dist-info/licenses/

- `LICENSE` — Project license (~290 tok)

## venv/Lib/site-packages/filelock/

- `__init__.py` (~747 tok)
- `_api.py` — URL configuration (~6099 tok)
- `_async_read_write.py` — Async wrapper around :class:`ReadWriteLock` for use with ``asyncio``. (~2217 tok)
- `_error.py` — Timeout: lock_file (~226 tok)
- `_read_write.py` — URL configuration (~4378 tok)
- `_soft.py` — SoftFileLock: pid, is_lock_held_by_us, break_lock (~2238 tok)
- `_unix.py` — : a flag to indicate if the fcntl API is available (~1308 tok)
- `_util.py` — raise_on_not_writable_file, ensure_directory_exists (~491 tok)
- `_windows.py` — Declares WindowsFileLock (~1127 tok)
- `asyncio.py` — An asyncio-based implementation of the file lock. (~4157 tok)
- `py.typed` (~0 tok)
- `version.py` — file generated by vcs-versioning (~150 tok)

## venv/Lib/site-packages/filelock/_soft_rw/

- `__init__.py` — Cross-process and cross-host reader/writer lock on :class:`~filelock.SoftFileLock` primitives. (~106 tok)
- `_async.py` — Async wrapper around :class:`SoftReadWriteLock` for use with ``asyncio``. (~2487 tok)
- `_sync.py` — Cross-process and cross-host reader/writer lock built on :class:`SoftFileLock` primitives. (~9975 tok)

## venv/Lib/site-packages/flask-3.1.3.dist-info/

- `entry_points.txt` (~10 tok)
- `INSTALLER` (~2 tok)
- `METADATA` (~845 tok)
- `RECORD` (~995 tok)
- `REQUESTED` (~0 tok)
- `WHEEL` (~22 tok)

## venv/Lib/site-packages/flask-3.1.3.dist-info/licenses/

- `LICENSE.txt` (~369 tok)

## venv/Lib/site-packages/flask/

- `__init__.py` (~772 tok)
- `__main__.py` (~9 tok)
- `app.py` — Flask: get_send_file_max_age (~17634 tok)
- `blueprints.py` — Flask blueprint (~1298 tok)
- `cli.py` — URL configuration (~10624 tok)
- `config.py` — ConfigAttribute: from_envvar, from_prefixed_env, from_pyfile, from_object + 3 more (~3777 tok)
- `ctx.py` — View: get (~4435 tok)
- `debughelpers.py` — UnexpectedUnicodeError: attach_enctype_error_multidict, explain_template_loading_attempts (~1738 tok)
- `globals.py` (~490 tok)
- `helpers.py` — API: GET (2 endpoints) (~6720 tok)
- `logging.py` — wsgi_errors_stream, has_level_handler, create_logger (~680 tok)
- `py.typed` (~0 tok)
- `sessions.py` — URL configuration (~4277 tok)
- `signals.py` — This namespace is only for signals provided by Flask itself. (~215 tok)
- `templating.py` — Environment: get_source, list_templates, render_template, render_template_string + 3 more (~2194 tok)
- `testing.py` — EnvironBuilder: json_dumps, session_transaction, open, invoke (~2891 tok)
- `typing.py` — Declares of (~941 tok)
- `views.py` — View: get, post (~1990 tok)
- `wrappers.py` — URL configuration (~2688 tok)

## venv/Lib/site-packages/flask/json/

- `__init__.py` — dumps, dump, loads, load + 1 more (~1601 tok)
- `provider.py` — JSONProvider: dumps, dump, loads, load + 4 more (~2192 tok)
- `tag.py` — Serializer: for (~2652 tok)

## venv/Lib/site-packages/flask/sansio/

- `app.py` — Declares App (~10888 tok)
- `blueprints.py` — Flask blueprint (~7040 tok)
- `README.md` — Project documentation (~57 tok)
- `scaffold.py` — View: get, post, put, delete (~8678 tok)

## venv/Lib/site-packages/fontTools/

- `__init__.py` (~55 tok)
- `__main__.py` — main (~275 tok)
- `afmLib.py` — Module for reading and writing AFM (Adobe Font Metrics) files. (~3887 tok)
- `agl.py` — -*- coding: utf-8 -*- (~33656 tok)
- `annotations.py` — Declares K (~359 tok)
- `fontBuilder.py` — is: drawTestGlyph, drawTestGlyph, usBreakChar, save + 4 more (~10084 tok)
- `help.py` — main (~332 tok)
- `tfmLib.py` — Module for reading TFM (TeX Font Metrics) files. (~4205 tok)
- `ttx.py` — Options: ttList, ttDump (~5074 tok)
- `unicode.py` — _UnicodeCustom: setUnicodeData (~368 tok)

## venv/Lib/site-packages/fontTools/cffLib/

- `__init__.py` — cffLib: read/write Adobe CFF fonts (~31881 tok)
- `CFF2ToCFF.py` — CFF2 to CFF converter. (~2417 tok)
- `CFFToCFF2.py` — CFF to CFF2 converter. (~2979 tok)
- `specializer.py` — T2CharString operator specializer and generalizer. (~9582 tok)
- `transforms.py` — StopHintCountEvent: execute, op_callsubr, op_callgsubr, stop_hint_count + 18 more (~5129 tok)
- `width.py` — T2CharString glyph width optimizer. (~1796 tok)

## venv/Lib/site-packages/fontTools/colorLib/

- `__init__.py` (~0 tok)
- `builder.py` — ColorPaletteType: populateCOLRv0, buildCOLR, buildClipList, buildClipBox + 2 more (~6970 tok)
- `errors.py` — Declares ColorLibError (~13 tok)
- `geometry.py` — Helpers for manipulating 2D points and vectors in COLR table. (~1617 tok)
- `table_builder.py` — BuildCallback: build, unbuild (~2198 tok)
- `unbuilder.py` — LayerListUnbuilder: unbuildColrV1, unbuildPaint (~636 tok)

## venv/Lib/site-packages/fontTools/config/

- `__init__.py` — Declares can (~927 tok)

## venv/Lib/site-packages/fontTools/cu2qu/

- `__init__.py` — you may not use this file except in compliance with the License. (~181 tok)
- `__main__.py` (~28 tok)
- `benchmark.py` — Benchmark the cu2qu algorithm performance. (~386 tok)
- `cli.py` — URL configuration (~1793 tok)
- `cu2qu.c` (~190620 tok)
- `cu2qu.cp313-win_amd64.pyd` (~26045 tok)
- `cu2qu.py` — cython: language_level=3 (~5376 tok)
- `errors.py` — you may not use this file except in compliance with the License. (~720 tok)
- `ufo.py` — Converts cubic bezier curves to quadratic splines. (~3860 tok)

## venv/Lib/site-packages/fontTools/designspaceLib/

- `__init__.py` — DesignSpaceDocumentError: posix, posixpath_property, getter, setter + 7 more (~38007 tok)
- `__main__.py` (~32 tok)
- `split.py` — Allows building all the variable fonts of a DesignSpace version 5 by (~5633 tok)
- `statNames.py` — Compute name information for a given location in user-space coordinates (~2714 tok)
- `types.py` — from: clamp, intersection, locationInRegion, regionInRegion + 2 more (~1562 tok)

## venv/Lib/site-packages/fontTools/diff/

- `__init__.py` — pipe_output, summarize, get_binary_exclude_tables, main + 1 more (~4020 tok)
- `__main__.py` (~29 tok)
- `color.py` — color_unified_diff_line (~409 tok)
- `diff.py` — Private functions (~2646 tok)
- `utils.py` — file_exists, get_file_modtime, get_tables_argument_list (~300 tok)

## venv/Lib/site-packages/fontTools/encodings/

- `__init__.py` — Empty __init__.py file to signal Python this directory is a package. (~22 tok)
- `codecs.py` — Extend the Python codecs module with a few encodings that are used in OpenType (name table) (~1388 tok)
- `MacRoman.py` (~1096 tok)
- `StandardEncoding.py` (~1097 tok)

## venv/Lib/site-packages/fontTools/feaLib/

- `__init__.py` — fontTools.feaLib -- a package for dealing with OpenType feature files. (~62 tok)
- `__main__.py` — main (~663 tok)
- `ast.py` — Element: deviceToString, asFea, build, asFea + 22 more (~21801 tok)
- `builder.py` — Builder: addOpenTypeFeatures, addOpenTypeFeaturesFromString, build, elif + 4 more (~22070 tok)
- `error.py` — Declares FeatureLibError (~192 tok)
- `lexer.c` (~218811 tok)
- `lexer.cp313-win_amd64.pyd` (~29631 tok)
- `lexer.py` — Lexer: next, location_, next_, scan_over_ + 5 more (~3260 tok)
- `location.py` — Declares FeatureLibLocation (~71 tok)
- `lookupDebugInfo.py` — Declares LookupDebugInfo (~91 tok)
- `parser.py` — Parser: parse, parse_anchor_, is, parse_anchor_marks_ + 5 more (~29249 tok)
- `variableScalar.py` — from: Location, does_vary, add_value, add_to_variation_store + 7 more (~2839 tok)

## venv/Lib/site-packages/fontTools/merge/

- `__init__.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~2430 tok)
- `__main__.py` (~29 tok)
- `base.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~706 tok)
- `cmap.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~1972 tok)
- `layout.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~4744 tok)
- `options.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~739 tok)
- `tables.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~3232 tok)
- `unicode.py` — is_Default_Ignorable (~1244 tok)
- `util.py` — Google Author(s): Behdad Esfahbod, Roozbeh Pournader (~1006 tok)

## venv/Lib/site-packages/fontTools/misc/

- `__init__.py` — Empty __init__.py file to signal Python this directory is a package. (~22 tok)
- `arrayTools.py` — Routines for calculating bounding boxes, point in rectangle calculations and (~3402 tok)
- `bezierTools.cp313-win_amd64.pyd` (~84090 tok)
- `bezierTools.py` — fontTools.misc.bezierTools.py -- tools for working with Bezier path segments. (~13353 tok)
- `classifyTools.py` — fontTools.misc.classifyTools.py -- tools for classifying things. (~1653 tok)
- `cliTools.py` — Collection of utilities for command-line interfaces and console scripts. (~548 tok)
- `configTools.py` — of: parse_optional_bool, validate_optional_bool, register, register_option + 6 more (~3309 tok)
- `cython.py` — Exports a no-op 'cython' namespace similar to (~203 tok)
- `dictTools.py` — Misc dict tools. (~715 tok)
- `eexec.py` — decrypt, encrypt, hexString, deHexString (~986 tok)
- `encodingTools.py` — fontTools.misc.encodingTools.py -- tools for working with OpenType encodings. (~613 tok)
- `enumTools.py` — Enum-related utilities, including backports for older Python versions. (~150 tok)
- `etree.py` — Shim module exporting the same ElementTree API for lxml and (~4789 tok)
- `filenames.py` — NameTranslationError: userNameToFileName, handleClash1, handleClash2 (~2420 tok)
- `fixedTools.py` — fixedToFloat, floatToFixed, floatToFixedToFloat, fixedToStr + 5 more (~2264 tok)
- `intTools.py` — bit_count, bit_indices (~175 tok)
- `iterTools.py` — Python 3.12: (~115 tok)
- `lazyTools.py` — Declares LazyDict (~304 tok)
- `loggingTools.py` — default logging level used by Timer class (~5851 tok)
- `macCreatorType.py` — getMacCreatorAndType, setMacCreatorAndType (~472 tok)
- `macRes.py` — ResourceError: openResourceFork, openDataFork, keys, types + 7 more (~2526 tok)
- `psCharStrings.py` — psCharStrings.py -- module implementing various kinds of CharStrings: (~12852 tok)
- `psLib.py` — PSTokenError: read, close, getnexttoken, skipwhite + 20 more (~3571 tok)
- `psOperators.py` — ps_object: put, ps_def, ps_bind, proc_bind + 34 more (~4650 tok)
- `py23.py` — Python 2/3 compat layer leftovers. (~667 tok)
- `roundTools.py` — noRound, otRound, maybeRound, roundFunc + 1 more (~938 tok)
- `sstruct.py` — sstruct.py -- SuperStruct (~2068 tok)
- `symfont.py` — _BezierFuncsLazy: green, printGreenPen (~2063 tok)
- `testTools.py` — Helpers for writing unit tests. (~2082 tok)
- `textTools.py` — fontTools.misc.textTools.py -- miscellaneous routines. (~1040 tok)
- `timeTools.py` — fontTools.misc.timeTools.py -- tools for working with OpenType timestamps. (~664 tok)
- `transform.py` — Affine 2D transformation matrix class. (~4662 tok)
- `treeTools.py` — Generic tools for working with trees. (~376 tok)
- `vector.py` — Vector: length, normalized, dot, toInt + 3 more (~1203 tok)
- `visitor.py` — Generic visitor pattern implementation for Python objects. (~1690 tok)
- `xmlReader.py` — TTXParseError: read, close, set, increment + 1 more (~1934 tok)
- `xmlWriter.py` — xmlWriter.py -- Simple XML authoring class (~2176 tok)

## venv/Lib/site-packages/fontTools/misc/filesystem/

- `__init__.py` — Minimal, stdlib-only replacement for [`pyfilesystem2`][1] API for use by `fontTools.ufoLib`. (~594 tok)
- `_base.py` — URL configuration (~1184 tok)
- `_copy.py` — copy_file, copy_structure, copy_dir, copy_fs (~402 tok)
- `_errors.py` — Declares FSError (~199 tok)
- `_info.py` — View: get (~597 tok)
- `_osfs.py` — URL configuration (~1686 tok)
- `_path.py` — URL configuration (~518 tok)
- `_subfs.py` — URL configuration (~892 tok)
- `_tempfs.py` — TempFS: close, clean (~274 tok)
- `_tools.py` — remove_empty, copy_file_data (~288 tok)
- `_walk.py` — BoundWalker: files, dirs (~489 tok)
- `_zipfs.py` — URL configuration (~1859 tok)

## venv/Lib/site-packages/fontTools/misc/plistlib/

- `__init__.py` — Data: fromBase64, asBase64, start, end + 16 more (~6227 tok)
- `py.typed` (~0 tok)

## venv/Lib/site-packages/fontTools/mtiLib/

- `__init__.py` — FontDame-to-FontTools for OpenType Layout tables (~13715 tok)
- `__main__.py` (~29 tok)

## venv/Lib/site-packages/fontTools/otlLib/

- `__init__.py` — OpenType Layout-related functionality. (~14 tok)
- `builder.py` — LookupBuilder: buildCoverage, buildLookup, equals, promote_lookup_type + 18 more (~38002 tok)
- `error.py` — Declares OpenTypeLibError (~99 tok)
- `maxContextCalc.py` — maxCtxFont, maxCtxSubtable, maxCtxContextualSubtable, maxCtxContextualRule (~935 tok)

## venv/Lib/site-packages/fontTools/otlLib/optimize/

- `__init__.py` — main (~453 tok)
- `__main__.py` (~32 tok)
- `gpos.py` — from: compact, compact_lookup, compact_ext_lookup, compact_pair_pos + 10 more (~5168 tok)

## venv/Lib/site-packages/fontTools/pens/

- `__init__.py` — Empty __init__.py file to signal Python this directory is a package. (~22 tok)
- `areaPen.py` — Calculate the area of a glyph. (~436 tok)
- `basePen.py` — fontTools.pens.basePen.py -- Tools and base classes to build pen objects. (~5014 tok)
- `boundsPen.py` — ControlBoundsPen: init (~922 tok)
- `cairoPen.py` — Pen to draw to a Cairo graphics library context. (~177 tok)
- `cocoaPen.py` — Declares CocoaPen (~183 tok)
- `cu2quPen.py` — you may not use this file except in compliance with the License. (~3810 tok)
- `explicitClosingLinePen.py` — ExplicitClosingLinePen: filterContour (~949 tok)
- `filterPen.py` — _PassThruComponentsMixin: addComponent, moveTo, lineTo, curveTo + 13 more (~4325 tok)
- `freetypePen.py` — Pen to rasterize paths with FreeType. (~5811 tok)
- `hashPointPen.py` — Modified from https://github.com/adobe-type-tools/psautohint/blob/08b346865710ed3c172f1eb581d6ef243b203f99/python/psautohint/ufoFont.py#L800-L838 (~1047 tok)
- `momentsPen.c` (~166325 tok)
- `momentsPen.cp313-win_amd64.pyd` (~21428 tok)
- `momentsPen.py` — Declares MomentsPen (~7582 tok)
- `perimeterPen.py` — Calculate the perimeter of a glyph. (~635 tok)
- `pointInsidePen.py` — fontTools.pens.pointInsidePen -- Pen implementing "point inside" testing (~1871 tok)
- `pointPen.py` — ReverseFlipped: beginPath, endPath, addPoint, addComponent + 9 more (~7217 tok)
- `qtPen.py` — URL configuration (~190 tok)
- `qu2cuPen.py` — you may not use this file except in compliance with the License. (~1169 tok)
- `quartzPen.py` — URL configuration (~380 tok)
- `recordingPen.py` — Pen recording operations that can be accessed or replayed. (~3664 tok)
- `reportLabPen.py` — Declares ReportLabPen (~613 tok)
- `reverseContourPen.py` — ReverseContourPen: filterContour, reversedContour (~1177 tok)
- `roundingPen.py` — RoundingPen: moveTo, lineTo, curveTo, qCurveTo + 3 more (~1358 tok)
- `statisticsPen.py` — Pen calculating area, center of mass, variance and standard-deviation, (~2892 tok)
- `svgPathPen.py` — SVGPathPen: pointToString, getCommands, main (~2538 tok)
- `t2CharStringPen.py` — Author: Tal Leming (~863 tok)
- `teePen.py` — Pen multiplexing drawing to one or more pens. (~385 tok)
- `transformPen.py` — TransformPen: moveTo, lineTo, curveTo, qCurveTo + 5 more (~1192 tok)
- `ttGlyphPen.py` — _TTGlyphBasePen: init, addComponent, glyph, lineTo + 9 more (~3488 tok)
- `wxPen.py` — URL configuration (~203 tok)

## venv/Lib/site-packages/fontTools/qu2cu/

- `__init__.py` — you may not use this file except in compliance with the License. (~181 tok)
- `__main__.py` (~29 tok)
- `benchmark.py` — Benchmark the qu2cu algorithm performance. (~416 tok)
- `cli.py` (~1134 tok)
- `qu2cu.c` (~214882 tok)
- `qu2cu.cp313-win_amd64.pyd` (~29129 tok)
- `qu2cu.py` — cython: language_level=3 (~3872 tok)

## venv/Lib/site-packages/fontTools/subset/

- `__init__.py` — Google Author(s): Behdad Esfahbod (~42103 tok)
- `__main__.py` (~29 tok)
- `cff.py` — _ClosureGlyphsT2Decompiler: op_endchar, closure_glyphs, prune_pre_subset, subset_glyphs + 4 more (~1809 tok)
- `svg.py` — URL patterns: 3 routes (~2729 tok)
- `util.py` — Private utility methods used by the subset modules (~223 tok)

## venv/Lib/site-packages/fontTools/svgLib/

- `__init__.py` (~23 tok)

## venv/Lib/site-packages/fontTools/svgLib/path/

- `__init__.py` — URL configuration (~589 tok)
- `arc.py` — Convert SVG Path's elliptical arcs to Bezier curves. (~1705 tok)
- `parser.py` — SVG Path specification parser. (~3175 tok)
- `shapes.py` — URL patterns: 2 routes (~1592 tok)

## venv/Lib/site-packages/fontTools/t1Lib/

- `__init__.py` — fontTools.t1Lib.py -- Tools for PostScript Type 1 fonts. (~6147 tok)

## venv/Lib/site-packages/fontTools/ttLib/

- `__init__.py` — fontTools.ttLib -- a package for dealing with TrueType fonts. (~198 tok)
- `__main__.py` — main (~1395 tok)
- `macUtils.py` — ttLib.macUtils.py -- Various Mac-specific stuff. (~512 tok)
- `removeOverlaps.py` — Simplify TrueType glyphs by merging overlapping contours/components. (~3754 tok)
- `reorderGlyphs.py` — Reorder glyphs in a font. (~3045 tok)
- `scaleUpem.py` — Change the units-per-EM of a font. (~4302 tok)
- `sfnt.py` — ttLib/sfnt.py -- low-level module to deal with the sfnt file format. (~6756 tok)
- `standardGlyphOrder.py` — 'post' table formats 1.0 and 2.0 rely on this list of "standard" (~1731 tok)
- `ttCollection.py` — TTCollection: close, save, saveXML (~1168 tok)
- `ttFont.py` — TTFont: close, save (~18456 tok)
- `ttGlyphSet.py` — GlyphSets returned by a TTFont. (~5134 tok)
- `ttVisitor.py` — Specialization of fontTools.misc.visitor to work with TTFont. (~302 tok)
- `woff2.py` — WOFF2Reader: reconstructTable, close (~17886 tok)

## venv/Lib/site-packages/fontTools/ttLib/tables/

- `__init__.py` — DON'T EDIT! This file is generated by MetaTools/buildTableList.py. (~754 tok)
- `_a_n_k_r.py` — Declares table__a_n_k_r (~143 tok)
- `_a_v_a_r.py` — table__a_v_a_r: compile, decompile, toXML, fromXML + 1 more (~2164 tok)
- `_b_s_l_n.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6bsln.html (~138 tok)
- `_c_i_d_g.py` — coding: utf-8 (~267 tok)
- `_c_m_a_p.py` — table__c_m_a_p: getcmap, getBestCmap, buildReversed, buildReversedMin + 8 more (~18326 tok)
- `_c_v_a_r.py` — table__c_v_a_r: compile, decompile, fromXML, toXML (~1035 tok)
- `_c_v_t.py` — table__c_v_t: decompile, compile, toXML, fromXML (~479 tok)
- `_f_e_a_t.py` — Declares table__f_e_a_t (~139 tok)
- `_f_p_g_m.py` — table__f_p_g_m: decompile, compile, toXML, fromXML (~485 tok)
- `_f_v_a_r.py` — table__f_v_a_r: compile, decompile, toXML, fromXML + 9 more (~2591 tok)
- `_g_a_s_p.py` — table__g_a_s_p: decompile, compile, toXML, fromXML (~648 tok)
- `_g_c_i_d.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6gcid.html (~108 tok)
- `_g_l_y_f.py` — _g_l_y_f.py -- Converter classes for the 'glyf' table. (~25031 tok)
- `_g_v_a_r.py` — table__g_v_a_r: compile, compileGlyphs_, decompile, get_read_item + 9 more (~3582 tok)
- `_h_d_m_x.py` — _GlyphnamedList: keys, decompile, compile, toXML + 1 more (~1252 tok)
- `_h_e_a_d.py` — table__h_e_a_d: decompile, compile, toXML, fromXML (~1445 tok)
- `_h_h_e_a.py` — table__h_h_e_a: ascender, ascender, descender, descender + 5 more (~1404 tok)
- `_h_m_t_x.py` — table__h_m_t_x: decompile, compile, toXML, fromXML (~1816 tok)
- `_k_e_r_n.py` — table__k_e_r_n: getkern, decompile, compile, toXML + 9 more (~3167 tok)
- `_l_c_a_r.py` — Declares table__l_c_a_r (~116 tok)
- `_l_o_c_a.py` — table__l_o_c_a: decompile, compile, set, toXML (~643 tok)
- `_l_t_a_g.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6ltag.html (~750 tok)
- `_m_a_x_p.py` — table__m_a_x_p: decompile, compile, recalc, testrepr + 2 more (~1546 tok)
- `_m_e_t_a.py` — Apple's documentation of 'meta': (~1150 tok)
- `_m_o_r_t.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6mort.html (~144 tok)
- `_m_o_r_x.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6morx.html (~161 tok)
- `_n_a_m_e.py` — -*- coding: utf-8 -*- (~12061 tok)
- `_o_p_b_d.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6opbd.html (~132 tok)
- `_p_o_s_t.py` — table__p_o_s_t: decompile, compile, getGlyphOrder, decode_format_1_0 + 10 more (~3426 tok)
- `_p_r_e_p.py` — Declares table__p_r_e_p (~127 tok)
- `_p_r_o_p.py` — https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6prop.html (~126 tok)
- `_s_b_i_x.py` — table__s_b_i_x: decompile, compile, toXML, fromXML (~1427 tok)
- `_t_r_a_k.py` — table__t_r_a_k: compile, decompile, toXML, fromXML + 9 more (~3338 tok)
- `_v_h_e_a.py` — table__v_h_e_a: decompile, compile, recalc, toXML + 3 more (~1314 tok)
- `_v_m_t_x.py` — Declares table__v_m_t_x (~149 tok)
- `asciiTable.py` — asciiTable: toXML, fromXML (~188 tok)
- `B_A_S_E_.py` — Declares table_B_A_S_E_ (~110 tok)
- `BitmapGlyphMetrics.py` — Since bitmap glyph metrics are shared between EBLC and EBDT (~524 tok)
- `C_B_D_T_.py` — Google Author(s): Matt Fontaine (~1074 tok)
- `C_B_L_C_.py` — Google Author(s): Matt Fontaine (~154 tok)
- `C_F_F__2.py` — table_C_F_F__2: decompile, compile (~238 tok)
- `C_F_F_.py` — table_C_F_F_: decompile, compile, haveGlyphNames, getGlyphOrder + 3 more (~583 tok)
- `C_O_L_R_.py` — Google Author(s): Behdad Esfahbod (~1760 tok)
- `C_P_A_L_.py` — Google Author(s): Behdad Esfahbod (~3500 tok)
- `D__e_b_g.py` — table_D__e_b_g: decompile, compile, toXML, fromXML (~334 tok)
- `D_S_I_G_.py` — table_D_S_I_G_: decompile, compile, toXML, fromXML + 3 more (~1736 tok)
- `DefaultTable.py` — DefaultTable: decompile, compile, toXML, fromXML (~565 tok)
- `E_B_D_T_.py` — table_E_B_D_T_: getImageFormatClass, decompile, compile, toXML + 3 more (~9534 tok)
- `E_B_L_C_.py` — table_E_B_L_C_: getIndexFormatClass, decompile, compile, toXML + 3 more (~8792 tok)
- `F__e_a_t.py` — table_F__e_a_t: decompile, compile, toXML, fromXML (~1610 tok)
- `F_F_T_M_.py` — table_F_F_T_M_: decompile, compile, toXML, fromXML (~496 tok)
- `G__l_a_t.py` — from itertools import * (~2538 tok)
- `G__l_o_c.py` — table_G__l_o_c: decompile, compile, set, toXML + 1 more (~792 tok)
- `G_D_E_F_.py` — Declares table_G_D_E_F_ (~90 tok)
- `G_P_O_S_.py` — Declares table_G_P_O_S_ (~118 tok)
- `G_S_U_B_.py` — Declares table_G_S_U_B_ (~88 tok)
- `G_V_A_R_.py` — Declares table_G_V_A_R_ (~29 tok)
- `grUtils.py` — decompress, compress, entries, bininfo + 2 more (~675 tok)
- `H_V_A_R_.py` — Declares table_H_V_A_R_ (~94 tok)
- `J_S_T_F_.py` — Declares table_J_S_T_F_ (~94 tok)
- `L_T_S_H_.py` — XXX I've lowered the strictness, to make sure Apple's own Chicago (~642 tok)
- `M_A_T_H_.py` — Declares table_M_A_T_H_ (~102 tok)
- `M_V_A_R_.py` — Declares table_M_V_A_R_ (~92 tok)
- `O_S_2f_2.py` — Panose: toXML, fromXML, decompile, compile + 12 more (~8210 tok)
- `otBase.py` — OverflowErrorRecord: decompile, compile, tryPackingHarfbuzz, tryPackingFontTools + 19 more (~15556 tok)
- `otConverters.py` — in: buildConverters, readArray, get_read_item, read_item + 44 more (~21816 tok)
- `otData.py` (~58183 tok)
- `otTables.py` — fontTools.ttLib.tables.otTables -- A collection of classes representing the various (~28475 tok)
- `otTraverse.py` — Methods for traversing trees of otData-driven OpenType tables. (~1624 tok)
- `S__i_l_f.py` — from itertools import * (~10293 tok)
- `S__i_l_l.py` — table_S__i_l_l: decompile, compile, toXML, fromXML (~948 tok)
- `S_T_A_T_.py` — Declares table_S_T_A_T_ (~147 tok)
- `S_V_G_.py` — Compiles/decompiles SVG table. (~2257 tok)
- `sbixGlyph.py` — Glyph: is_reference_type, decompile, compile, toXML + 1 more (~1699 tok)
- `sbixStrike.py` — Strike: decompile, compile, toXML, fromXML (~1951 tok)
- `T_S_I__0.py` — TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT) (~736 tok)
- `T_S_I__1.py` — TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT) (~2039 tok)
- `T_S_I__2.py` — TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT) (~147 tok)
- `T_S_I__3.py` — TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT) (~162 tok)
- `T_S_I__5.py` — TSI{0,1,2,3,5} are private tables used by Microsoft Visual TrueType (VTT) (~562 tok)
- `T_S_I_B_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~102 tok)
- `T_S_I_C_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~113 tok)
- `T_S_I_D_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~102 tok)
- `T_S_I_J_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~102 tok)
- `T_S_I_P_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~102 tok)
- `T_S_I_S_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~102 tok)
- `T_S_I_V_.py` — TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT) (~252 tok)
- `T_T_F_A_.py` — Declares table_T_T_F_A_ (~116 tok)
- `table_API_readme.txt` — Declares table__g_l_y_f (~710 tok)
- `ttProgram.py` — ttLib.tables.ttProgram.py -- Assembler/disassembler for TrueType bytecode programs. (~10458 tok)
- `TupleVariation.py` — TupleVariation: getUsedPoints, hasImpact, toXML, fromXML + 7 more (~9452 tok)
- `V_A_R_C_.py` — Declares table_V_A_R_C_ (~86 tok)
- `V_D_M_X_.py` — table_V_D_M_X_: decompile, compile, toXML, fromXML (~3054 tok)
- `V_O_R_G_.py` — table_V_O_R_G_: decompile, compile, toXML, fromXML + 2 more (~1752 tok)
- `V_V_A_R_.py` — Declares table_V_V_A_R_ (~95 tok)

## venv/Lib/site-packages/fontTools/ufoLib/

- `__init__.py` — URL patterns: 1 routes (~29016 tok)
- `converters.py` — convertUFO1OrUFO2KerningToUFO3Kerning, findKnownKerningGroups, makeUniqueGroupName, test (~3958 tok)
- `errors.py` — Declares UFOLibError (~250 tok)
- `etree.py` — DEPRECATED - This module is kept here only as a backward compatibility shim (~68 tok)
- `filenames.py` — NameTranslationError: userNameToFileName, handleClash1, handleClash2 (~3146 tok)
- `glifLib.py` — URL patterns: 1 routes (~22748 tok)
- `kerning.py` — lookupKerningValue (~1422 tok)
- `plistlib.py` — DEPRECATED - This module is kept here only as a backward compatibility shim (~445 tok)
- `pointPen.py` — DEPRECATED - This module is kept here only as a backward compatibility shim (~72 tok)
- `utils.py` — This module contains miscellaneous helpers. (~943 tok)
- `validators.py` — Various low level data validators. (~9483 tok)

## venv/Lib/site-packages/fontTools/unicodedata/

- `__init__.py` — mirrored, script, script_extension, script_name + 7 more (~2684 tok)
- `Blocks.py` — -*- coding: utf-8 -*- (~9702 tok)
- `Mirrored.py` — -*- coding: utf-8 -*- (~2768 tok)
- `OTTags.py` — Data updated to OpenType 1.8.2 as of January 2018. (~356 tok)
- `ScriptExtensions.py` — -*- coding: utf-8 -*- (~8422 tok)
- `Scripts.py` — -*- coding: utf-8 -*- (~38510 tok)

## venv/Lib/site-packages/fontTools/varLib/

- `__init__.py` — Declares only (~16674 tok)
- `__main__.py` (~29 tok)
- `avarPlanner.py` — main (~34 tok)
- `builder.py` — VariationStore (~1950 tok)
- `cff.py` — addCFFVarStore, convertCFFtoCFF2, conv_to_int, get_private + 4 more (~6724 tok)
- `errors.py` — VarLibError: reason, offender, details, details + 5 more (~2044 tok)
- `featureVars.py` — Module to build FeatureVariation tables: (~7681 tok)
- `hvar.py` — add_HVAR, add_VVAR, main (~1088 tok)
- `interpolatable.py` — Glyph: draw, test_gen, grand_parent (~13268 tok)
- `interpolatableHelpers.py` — InterpolatableProblem: sort_problems, rot_list, addComponent, beginPath + 14 more (~3042 tok)
- `interpolatablePlot.py` — OverridingDict: show_page, add_title_page, draw_legend, add_summary (~13011 tok)
- `interpolatableTestContourOrder.py` — test_contour_order (~872 tok)
- `interpolatableTestStartingPoint.py` — test_starting_point (~1278 tok)
- `interpolate_layout.py` — interpolate_layout, main (~1090 tok)
- `iup.c` (~244484 tok)
- `iup.cp313-win_amd64.pyd` (~34182 tok)
- `iup.py` — iup_segment, iup_contour, iup_delta, can_iup_in_between + 1 more (~4422 tok)
- `merger.py` — Merger: merger, wrapper, mergersFor, mergeObjects + 7 more (~17863 tok)
- `models.py` — Variation fonts interpolation models. (~6736 tok)
- `multiVarStore.py` — OnlineMultiVarStoreBuilder: setModel, setSupports, finish, storeMasters + 12 more (~2446 tok)
- `mutator.py` — interpolate_cff2_PrivateDict, interpolate_cff2_charstrings, interpolate_cff2_metrics, instantiateVariableFont (~5810 tok)
- `mvar.py` (~712 tok)
- `plot.py` — Visualize DesignSpaceDocument and resulting VariationModel. (~2210 tok)
- `stat.py` — Extra methods for DesignSpaceDocument to generate its STAT table data. (~1418 tok)
- `varStore.py` — OnlineVarStoreBuilder: setModel, setSupports, finish, storeMasters + 12 more (~7088 tok)

## venv/Lib/site-packages/fontTools/varLib/avar/

- `__init__.py` (~0 tok)
- `__main__.py` — main (~527 tok)
- `build.py` — build, main (~620 tok)
- `map.py` — map, main (~1031 tok)
- `plan.py` — normalizeLinear, interpolateLinear, normalizeLog, interpolateLog + 8 more (~8103 tok)
- `unbuild.py` — mappings_from_avar, unbuild, main (~3084 tok)

## venv/Lib/site-packages/fontTools/varLib/instancer/

- `__init__.py` — Partially instantiate a variable font. (~22135 tok)
- `__main__.py` (~32 tok)
- `featureVars.py` — instantiateFeatureVariations (~2086 tok)
- `names.py` — Helpers for instantiating name table records. (~4383 tok)
- `solver.py` — rebaseTent (~3232 tok)
