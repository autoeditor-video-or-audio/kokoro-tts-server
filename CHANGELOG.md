# [0.6.0](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.5.0...v0.6.0) (2026-10-01)


### Bug Fixes

* **api:** turn off CORS credentials for starlette 1.x ([abcb9cf](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/abcb9cfe0ba00ceae82d0fc1e1d18f84ebe83f1a))
* **audio:** drop WAV close()-time junk trailer that caused chunk-end click ([#467](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/467)) ([7649d86](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/7649d86b5f239db3ffe35aa7d4d111d9f21cebc7)), closes [#463](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/463)
* **audio:** implement audio file source swapping for stream playback and seeking ([#475](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/475)) ([2153529](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/21535295f314e97ca9289d94709b82cba66eca2c))
* **audio:** improve error handling for aborted audio streams ([106cbd4](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/106cbd4c4d939b472880c08f965c108ba09ccd00))
* **audio:** read finalize buffer before close except for ogg, fixes flac tail loss ([#497](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/497)) ([ef13810](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/ef13810b8bf8064104d28be77b772c4ae011e1bd))
* **changelog:** update model validation details for consistency and error handling ([3eb9606](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/3eb960674b91864de099bc5e070b2e5994784696))
* **chunking:** replace regex sentence splitter with UAX [#29](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/29) segmentation ([#308](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/308), adapts [#415](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/415)) ([#520](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/520)) ([d2aae10](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/d2aae102c0c6ba46770a1cf9c7b86bc0c64342a8))
* **ci:** run the test job with the cpu extra ([c6398b9](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c6398b98ab20128f387179452b048b212140613f))
* **debug-endpoints:** gate /debug/* introspection routes behind ENABLE_DEBUG_ENDPOINTS, documentation ([316aa67](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/316aa672ad56eee5f5f28d9345d7d0c14be39471))
* **dependencies:** update fastapi to 0.116.1 and pin starlette dependency to avoid CVE ([c2687ec](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c2687ec333ad7dd761d6f817a4e1641c72f64fc6))
* **dev-unload:** Prevent POST /dev/unload behind an opt-in setting ([#483](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/483)) ([24ac58e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/24ac58e1a0ab74127238ed1aa9609b6f85d3327c)), closes [#478](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/478)
* **docker:** aligns cu128 base image with wheel (12.9.1 → 12.8.1), minimum toolkit with Blackwell (sm_120) support (CUDA 12.8) ([0d6b4d8](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/0d6b4d89193bd18fc2bba47366a77db011143ab8)), closes [#306](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/306) [#320](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/320) [#389](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/389) [#443](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/443) [#365](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/365)
* **docker:** compose defaults to idempotent model download; harden download_model scripts, static release artifact link ([0cf239e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/0cf239ef55e4040a04bd84a5515ba055017246fd))
* **docker:** honour HOST/PORT in entrypoint for IPv6 binds ([#408](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/408)), download_model defaults; drop api dev mount cruft ([#522](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/522)) ([21a78e0](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/21a78e08329618d091bbfd7c37114e596401ea3c))
* **download_model:** checksum verification for downloaded model files, avoid clobbering pre-existing model files ([aab59af](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/aab59afc1301261bb3584a4ba0aee3d6787e49be))
* honour default_voice_code in _split_multi_voice (issue [#514](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/514)) ([#515](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/515)) ([5ba470b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5ba470b4b8254d891f0e8e982fb22260a39ba329))
* int16 overflow in silence-trim, invalid-escape in URL regex ([64cb068](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/64cb068438229fa49b5de13bc5fe109a288b1fb3))
* **mappings:** /v1/audio/voices returns id/name objects ([#462](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/462)) to align with OpenWebUI ([7bbd3a8](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/7bbd3a8e43380cf53fef8984395ff5c62c471b2f))
* **mappings:** update voice mappings for consistency, add missing audio file for 'bf_isabella' ([#480](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/480)) ([c5ccfa1](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c5ccfa1821522fc6d5af319ef36c3e85227145e7))
* **normalizer:** 'F' is normalised to "farad" instead of "fahrenheit" ([#526](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/526)) ([f901ed8](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/f901ed81ff9910b80ab24f800a245873221a5445))
* **normalizer:** anchor decimal regex to prevent backtracking on digit floods ([af6e444](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/af6e4440f473110afc3d7d6bbde5cbbceecce833))
* **normalizer:** expand apostrophe-less "'re" contractions ([7746fbe](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/7746fbe6d74480dcc3066ba0df74f3c1f4b1cf9d)), closes [#488](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/488) [#488](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/488)
* **normalizer:** expand wh-word 're contractions espeak voices as -ray ([#488](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/488)) ([f3a88ab](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/f3a88abb4d8a74df39c4b6564de417f8a7744c5c))
* **normalizer:** handle double dashes in text normalization and improve token processing ([4f826d6](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/4f826d6a02fd2aa12da75930b289fccf297bb24d))
* **normalizer:** handle version-like numbers before NUMBER_PATTERN splits ([a736569](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/a7365695a3e4f4fc442e7a46ba658979486d1560))
* **normalizer:** move range sub before NUMBER_PATTERN to fix minus handling ([6c5773d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/6c5773d53c48bde546324bd5683bc8ca7924bda5))
* **normalizer:** treat underscore as a word boundary in caps detection ([123580c](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/123580c5ca0f583eed7b44bed10668184e1ede7a))
* **paths:** allow operator symlinks in search roots, keep traversal containment ([9dac665](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/9dac6657f96cf58ac1a5614bc4485fa3dae452e5))
* **paths:** harden _find_file to stay contained to its search roots ([0cb3a0d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/0cb3a0d6ad1cdcdd623df33b66a9c255e6018b69))
* phonemes default voice code ([#516](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/516)) ([9138d89](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/9138d8995f9118125ded3bc925388f7f36282eb8))
* preserve paragraph breaks as sentence boundaries in normalizer ([#525](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/525)) ([fbbaa75](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/fbbaa75e89ff362f70d13562ad97d60f963ff6e4)), closes [#519](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/519)
* prevent ReDoS in text normalizer (URL/email/acronym patterns) ([#489](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/489)) ([5fb4753](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5fb4753dda896cf975fd545809c4eb466e288eea))
* **rocm:** persist MIOpen cache and add FIND_MODE=2 default +warmup script ([#469](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/469)) ([8ce0821](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8ce082126d5e5959c0a51834b20684d305b8d658))
* **schema, pause overflow:** caps total pause duration, input length, volume_multiplier, validates lang_code ([#511](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/511)) ([316409d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/316409d7bf59a7ffd5ee13410b7670dd809b8ba1))
* **server_addons:** run KOKORO_SYNC_ON_START sync inside the upstream lifespan ([39f1f6d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/39f1f6daebdc0f8033d069bffc14da554c5e100b)), closes [#1](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/1)
* **ssml, web:**  SSML root validation, rate validation in VoiceSelector ([5d54647](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5d5464749fa4e6c2027c5080e3e6c4e210bffd98))
* **ssml:** keep block boundaries, drop <desc>, add provider corpus, translate documents with an xml prolog, refuse DTDs, 400 on deep nesting,  cap nesting depth ([ffb4040](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/ffb4040bdf3c0f544b48b280e3cbb4c3e2bff2e5))
* **streaming:** close audio writer and generator on client disconnect ([#288](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/288), [#337](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/337)) ([#533](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/533)) ([cf8d71e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/cf8d71ef0e1d70891d1b0351307279dc77e483ed))
* **tests:** lazy import integration reqs, exclude on CI ([94f729f](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/94f729f8bfb5f4fc238da23a7e9fe78487cdead5))
* **tuning:** decode reference clips in a child process, serialized tune requests ([e498565](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/e498565be3c89c96b38f3380e2b9930118b07bcb))
* **uv direct run deps:** pyopenjtalk-plus on native Windows, avoids MSVC ([#508](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/508)); pending swapover after multi-platform image testing ([8b0a51c](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8b0a51c95ea4c974cb503b0ea07696068ce04512))
* **voices:** combine endpoint accepts weighted syntax, matching speech endpoints ([#285](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/285)) ([#512](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/512)) ([fdbcf96](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/fdbcf96003bf4ae6caadbbec6bc60777512022ae))
* **web download:**  voice-timestamp as download names, associated url handling ([5ba5190](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5ba5190f14d407a0450a3866fd30f01386f5fa28))
* **web:** add Firefox-safe audio playback fallback when MSE MP3 is unsupported ([5e55b5c](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5e55b5c05023c9a2338c4c4594522b75599cda84))
* **web:** anchor the cast menu to its Options button, float it in the top layer ([86662e3](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/86662e34caa5200b0d02824b495aecea791df598))
* **web:** assorted UI tweaks, responsiveness, animation ([91cd44d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/91cd44d6805dc04b8945871988ef354cd6d0ca9e))
* **web:** drop auto-insert voice tag, enter key to save name, update related tests ([1b66dde](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/1b66ddefb3c9971a04b236d26075aa846bac3983))
* **web:** filtering, edit mode opens name as well ([db46865](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/db46865932821e6d3d1afd72ae3e866b74188c87))
* **web:** firefox/supported playback handling and msging, bmac link, waveform bugfix ([a10fc75](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/a10fc75da14ee0a8e5e157ae43249f9ae2561390))
* **web:** pin playbar to bottom on slim view, responsive fixes, redesign tweaks ([328b816](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/328b8168ff0bf7eb13a00fb9577df026d9f765de))
* **web:** playback slider step size; smoothness ([89850a9](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/89850a982cc1a98af7cd2a6fd63f3aa336a3b2e5))
* **webui:** bounded buffer to resolve 10 minute crashout, player state short ciruit on no-up updates to preserve responsiveness on long sessions. ([#471](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/471)) ([3f64dc2](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/3f64dc26081dcb79e4d04ecb3d88da263be76964))
* **web:** voice search dropdown keys, clearable alias name, focus restore guard ([4aa5f1a](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/4aa5f1ad6f1822bbd918eb57649451c34f6d3cdd))
* word timestamps for non-English (espeak) voices in captioned_speech ([#484](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/484)) ([c0acb91](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c0acb91e441b80062bd2ed6a54b5d88862df5d06)), closes [#331](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/331)


### Features

* **api, web ui:** include voice grades on the voice listing endpoint ([#517](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/517)) ([5fb71ea](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5fb71ea6e75379f95dee0f4a42c12152f4ea0e1a))
* **api:** add POST /dev/unload to release model from GPU VRAM ([#474](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/474)) ([ff6efaf](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/ff6efaffa380df69b8c7a599d48945f619093376)), closes [#473](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/473)
* **api:** optional model auto-unload after idle timeout ([#506](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/506)) ([8307b0e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8307b0e576849201790b72ef9e70e059f39b6103))
* **benchmarks:** add model unload benchmarking script and update README with VRAM reclaim details ([6b58b53](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/6b58b53068f1927dd60c004e6ef5267452b1cd90))
* **gpu:** adds clear cu128 opt-in via compose, setup for Blackwell ([f08279f](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/f08279fb242e10f8663e074f69727f1ea1e868a9))
* **gpu:** adds clear cu128 opt-in via compose, setup for Blackwell / RTX 50-series release image ([65ef3b8](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/65ef3b8106e0b443d82527fcdb9dff34cc23d688))
* improve voice selector and tag handling ([e65f1ba](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/e65f1ba95bb2c089580a36db3f173bcc5353640b))
* **multi-speaker:** add inline multi-speaker support, voice alias mappings, read-along scrobbing in web ui ([#502](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/502)) ([5775958](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/577595854864fa014b041f5120a84810558942dc)), closes [#272](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/272)
* **normalizer:** caps_normalization option, spoken phone numbers, hertz plurals, drop the 'S pass, emoji tag flags and joiners, web toggles ([#353](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/353)) ([794a27b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/794a27b632d21ca687696c57b5070555ca637c3e))
* **normalizer:** opt-in remove_emoji, 400 before streaming on unspeakable input ([#353](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/353)) ([c3cb020](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c3cb020f72a98e335db21f1612bbf5732c755218))
* **player:**  duration handling and update UI controls for audio playback ([a559254](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/a5592542514b8ee424081900b700bcc25e4c58bf))
* **ssml, cleanup:** ENABLE_SSML kill switch, drop legacy settings, documentation of config variables) ([60d6862](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/60d6862adfd9ec4596ea79c17359e91557414868))
* **ssml, speed/rate tag:** initial crack at integrating speed param per voice, ssml compliance ([8e4810a](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8e4810a4a19bb664da42774ad547781e3b390357))
* **ssml:** adjust rate tag semantics to scale speaking pace and introduce baserate tag ([536bc76](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/536bc769fa80512fff9af99f20bdc28d1d35ebea))
* **ssml:** dedicated ssml router, shared rate clamp contract, alias rate visible + synced in web editor ([e282b40](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/e282b40abebd0c24140d4526ce4842a44764587f))
* **ssml:** ssml flag on the speech endpoints, one call to translate and synthesize ([719f47a](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/719f47a25f823cb6329cf572160a0284563a2be6))
* **time-to-first-audio:** lazy phonemization in get_sentence_info ([#513](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/513)) ([61be98d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/61be98db0e4a901e5387518ba31e75878351049a))
* **voice-clone-tune:** integrate Inno tuner, improve web ui ([e3049b2](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/e3049b22855519b7fbac0625e810d3c81d5a3b7e))
* **web,accessibility:** enhance keyboard navigation and ARIA attributes for improved accessibility ([8322a9b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8322a9bb64998b151e1053a3827392f07631270f))
* **web:** add cast pins, resize insert button and ordering ([ffa52e1](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/ffa52e106383b1eb201b71c954c2ce3a95ed634c))
* **web:** add duplicate to options, simplify suggested cast name rate to 3 digits ([fe9c7ae](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/fe9c7ae98f7f7e6e9be7d8b86728dd1d1a0a1d19))
* **web:** add text normalization toggle to web UI settings ([#523](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/523)) ([e57216c](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/e57216c0e767f11afa8deb7320657ce3d8d1b131))
* **web:** improve styling, responsiveness ([c53efd5](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c53efd5e9d65ca5a0aa59920f733710fabba1dca))
* **web:** normalization options menu in player ([de18072](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/de180722980816a819741e7114e0ba49bdd822ae))
* **web:** seamless auto swap-to-file ([c82946a](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c82946aab644f7285fc025040d48295449f03d54))
* **web:** show server version badge in the UI footer ([8e1bafe](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8e1bafe4be2f6d7e97843ebf8046519895d6b789))
* **web:** swap to the finished file as soon as it exists, allow minor skip on swap/ ([8cb69ac](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8cb69aca5d3a5c6b18a4948f4fa2740a4efe960b))
* **web:** voice list sorted by grade then name, DEFAULT_VOICE honoured ([5fec3ad](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5fec3ad2e6c67d20716e98e48a05e6f5a89baf42))


### Performance Improvements

* **rocm:** disable MIOpen by default, add ENABLE_MIOPEN opt-in ([#518](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/518)) ([5fc3ba3](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/5fc3ba31126c353e574c48cdd85cce1a24dfe784))

# [0.5.0](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.4.1...v0.5.0) (2026-05-14)


### Features

* **docker,ci,docs:** add CPU flavour alongside GPU ([47c079b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/47c079b0da60bd7604542706c03096336618dd90))

## [0.4.1](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.4.0...v0.4.1) (2026-05-14)


### Bug Fixes

* **save-combined:** parse weight syntax + compute weighted blend ourselves ([435338e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/435338e816bb1efe39c9606fedde701c20732d62))

# [0.4.0](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.3.2...v0.4.0) (2026-05-14)


### Features

* **server_addons:** POST /v1/voices/save-combined persists blends in voices_dir ([7d30c63](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/7d30c6392dae9f9e6c3ef4261d7d31129dd8a9c8))

## [0.3.2](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.3.1...v0.3.2) (2026-05-14)


### Bug Fixes

* **docker:** seed mounted voices_dir from baked voicepacks at boot ([4c0ffee](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/4c0ffeec757b1815ad7c79e6739ef070cf9d2162))

## [0.3.1](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.3.0...v0.3.1) (2026-05-14)


### Bug Fixes

* **docker:** use uv pip / uv run instead of bare .venv/bin/pip ([961d82d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/961d82d50be33efd282f33c12e3d92ae25de33a3))

# [0.3.0](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/compare/v0.2.4...v0.3.0) (2026-05-14)


### Bug Fixes

* Add reverse proxy support for web-ui ([213d8d5](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/213d8d56cb7d53dd55b4faa46c2fc03cc6aa09a0))
* **arm-triton-dep:** allow uv to choose valid triton target for gpu build ([8c9550e](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/8c9550e91817e4a13d82734ac0437d7b6595b286))
* cache voice tensors to prevent per-request memory leak ([b32d6b4](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/b32d6b4d89f4e87feefce5f5503a73fa0997d0ac)), closes [#453](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/issues/453)
* clear voice cache on unload, correct temp file age check, align tests ([a82860b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/a82860bbcc7b0296928a2d436f80a27be8d65709))
* OGG/Opus truncation — close container before reading buffer ([3970312](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/397031218bdcac7b95331f085260841d2791df56)), closes [remsky/Kokoro-FastAPI#447](https://github.com/remsky/Kokoro-FastAPI/issues/447)
* **tests:**  drop tautological load_model_validation ([c84adf3](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/c84adf35567a58d61843768869421adcd5370437))
* **triton-buld-dep:** add override deps for linux arch64 ([6c1b8bf](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/6c1b8bf36c1da8ddb4aeb6fe694a4f5db2d6805a))
* update PyTorch CUDA version from cu129 to cu126 ([d29dcf7](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/d29dcf76cfaae6fe559203b1ef7d45713dc28a21))
* use weights_only=True for voice tensor torch.load calls ([878fd5d](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/878fd5d02857e77d7594b7f0f125ae0cf464d154)), closes [remsky/Kokoro-FastAPI#452](https://github.com/remsky/Kokoro-FastAPI/issues/452)


### Features

* add configurable logging level with environment variable support ([43a069b](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/43a069b41f746dc8d57ad1803fee3368f3c3468b))
* nifty-star sibling-fork layer (server_addons, MinIO sync, ops parity) ([4133cb7](https://github.com/autoeditor-video-or-audio/kokoro-tts-server/commit/4133cb7ad53c924a0c1c0ef77aac27e4dc51393b))

# Changelog

Notable changes to this project will be documented in this file.

Per-PR attribution and contributor credits are published automatically on the corresponding GitHub release page; this file is the curated, human-readable summary.

## [v0.9.0] - 2026-09-09
### Added
- Voice clone-tuning from a short reference clip via [inno-kokoro](https://github.com/remsky/inno-kokoro):
  - `POST /dev/tune` speaks with the tuned voice (passes through to `/v1/audio/speech`) or returns the `.pt` via `return_voice_pack=true`,
  - When `ALLOW_LOCAL_VOICE_SAVING=true`, saves it as `<name>_tuned` with `save_voice=<name>`.
  - Off by default, requires `ENABLE_INNO_TUNER=true`. See [docs/inno-tune.md](docs/inno-tune.md).
- Web player: Tune tab (record or upload a clip, generate, download or save the pack).
- Four tuned voices bundled with `_inno` suffix:
  - `af_amelia_inno`, `af_goodall_inno`, `am_price_inno`, `bm_atten_inno`.
- `normalization_options.remove_emoji`, off by default: drop emoji instead of reading their names (#353).
- `normalization_options.caps_normalization`, on by default: all-caps names and headers read as words, short acronyms (`FBI`) still spelled.

### Changed
- Normalizer split into per-language classes, registry keyed by lang code.
  - CONTRIBUTING.md documents standardized contract to add additional languages
- `DEFAULT_VOICE` applies to requests that omit a voice, not just warmup. Reported as `default_voice` on `/v1/audio/voices`.
- Web player:
  - normalize checkbox replaced by a menu with every `normalization_options` field;
  - voice list sorted by grade then name, `DEFAULT_VOICE` preselected.

### Fixed
- Aborting a stream mid-playback no longer segfaults the server on a follow-up request with a new lang_code engine (#288, #337).
- Blank lines end a sentence, single newlines still join (#519, #525 by @Christian-Sidak).
- Very long unpunctuated non-English text no longer truncates.
- Blank or emoji-only input is a 400 on the streaming path too, not an empty 200.
- Web player: voice search and alias minor fixes.
- Normalization fixes:
  - Number reading: `3,497` as thousands not a year (#259);
  - `MP3`, `B2B`, `v1.0`, `COVID-19` read as written;
  - `.5` as zero point five; long digit runs no longer stall or 500.
  - Phone numbers, `3.5 GHz`, `1 min` (with `unit_normalization`), `DVDs`/`DVD's`, `12:30:15 pm` read correctly.
  - `--` reads as a dash and no longer fuses words or drops word timestamps (#249).

## [v0.8.2] - 2026-09-05
### Added
- Optional model auto-unload after an idle timeout (`MODEL_AUTO_UNLOAD_TIMEOUT_SECONDS`, default off) to release VRAM. Reloads on the next request. `/dev/model` reports load/idle state and `POST /dev/reload` pre-warms the model, both behind `ALLOW_DEV_UNLOAD`.
- `/v1/audio/voices` entries carry the per-voice grades from [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md), where graded; added in web player dropdown w/ hover for the target quality and training duration.
- Web player: `Normalize text` toggle in settings, off sends input as written (#391, #523 by @webdevsamran).

### Changed
- Sentence splitting via UAX #29 segmentation instead of regex; e.g: `etc.`, `Dr.`, and CJK punctuation split more accurately (#308, adapts #415 by @lionel-rowe).
- ROCm: MIOpen off by default for better performance re: tensor shape recompilation (2.4s vs 0.27s on gfx1100). `ENABLE_MIOPEN=true` restores it (#518 by @s-kerdel).
- Compose files no longer mount `api/` or set defaults already baked into the image (`DOWNLOAD_MODEL`, `PYTHONPATH`, etc).

### Fixed
- `DEFAULT_VOICE_CODE` now applies on the speech endpoints and `/dev/generate_from_phonemes` (#514, #515 by @Christian-Sidak, #516).
- Entrypoint and `start-*.sh` honour `HOST` / `PORT`, so `HOST=::` binds IPv6-only (#408, reported by @felixls).

## [v0.8.1] - 2026-08-24
### Fixed
- `/v1/audio/voices/combine` accepts weighted syntax (`af_bella(2)+af_sky(1)`), matching the speech endpoints (#285).
- Oversized or pause-heavy requests now return 400 to avoid exhausting memory (reported by @sshpie, GHSA-f64g-9jmv-pm22). Two new configurable limits:
  - `MAX_INPUT_LENGTH` (default 1_000_000) caps characters of text per request.
  - `MAX_TOTAL_PAUSE_S` (default 300) caps total `[pause:Ns]` / SSML `<break>` silence per request.
- Native Windows installs (`start-cpu.ps1` etc) no longer need a C++ toolchain: `pyopenjtalk-plus` (a drop-in fork with prebuilt Windows wheels) replaces `pyopenjtalk` on win32 only (#508, proposed by @siliconfps). Needs a recent `uv`. Linux, macOS, and Docker are unchanged.

### Changed
- Documented `WEB_CONCURRENCY` (uvicorn worker count) in `docs/configuration.md` for parallel model loads/concurrency (#115, #358).
- Improved time-to-first-audio; sentence phonemization emits to avoid a first full-request pass. Some gradual latency growth at larger input sizes due to normalization pass.

<div align="center">

|   Input    | v0.8.0 (eager) | v0.8.1 (lazy) |     |
|:-----------|---------------:|--------------:|----:|
| 5k chars   |         0.31 s |        0.26 s | -16% |
| 10k chars  |         0.30 s |        0.27 s | -10% |
| 50k chars  |         0.45 s |        0.29 s | -36% |
| 100k chars |         0.73 s |        0.31 s | -58% |
| 250k chars |         1.41 s |        0.45 s | -68% |
| 500k chars |         2.78 s |        0.56 s | -80% |
| 1M chars   |         5.21 s |        0.85 s | -84% |

</div>

## [v0.8.0] - 2026-08-14
### Added
- Multi-speaker input on `/v1/audio/speech` and `/dev/captioned_speech` (#294). Opt in per request with `allow_voice_tags: true`; disable server-wide with `ENABLE_VOICE_TAGS=false`.
  - Inline `[voice:name]` tags switch speaker mid-text.
  - `voice_aliases` mapping for named weighted voice mixes, with optional per-alias `rate`.
  - `/dev/captioned_speech` timestamps carry the resolved `voice` per word; the field is absent unless `allow_voice_tags` is on, so existing responses are unchanged.
- `POST /dev/dialogue` for ordered multi-speaker turns.
- SSML input (experimental). Disable server-wide with `ENABLE_SSML=false`.
  - `ssml: true` on `/v1/audio/speech` and `/dev/captioned_speech` translates and speaks in one call. Requires `allow_voice_tags: true`, since the translation emits `[voice:]` and `[rate:]` spans.
  - `POST /dev/ssml` returns the translated tokens as text instead, for inspecting them before synthesis.
- `return_timing` on `/v1/audio/speech`: per-chunk `{text, start, end}` JSON sidecar next to the download (powers the web reader).
- `MAX_PAUSE_DURATION_S` (default 60) caps a single `[pause:Ns]` tag or SSML `<break>`.
- Web UI:
  - Voice alias/tag cast builder with import/export, pinning, and per-alias rate, synced with the editor (re: parallel work by @radzrader, [#272](https://github.com/remsky/Kokoro-FastAPI/discussions/272)).
  - Read-along mode: sentence highlighting synced to playback, bidirectional click to seek.
  - Find/replace across pages, direct page-number entry, download menu (audio / timings / both).
- Wiki pages moved into `docs/`, versioned alongside the code.

### Changed
- Docker images compile to bytecode at build, ~40% faster startup.
- Containers launch uvicorn directly rather than through `uv run`, which resolves startup permission failures on Unraid and similar hosts.
- `[rate:]` tags scale the speaking voice's alias rate instead of replacing it, so a voice calibrated to 0.8 stays proportionally slower under `[rate:1.1]`. Matches how SSML engines treat rate.
- Speed bounds (0.25 to 4.0) shared across speed fields and SSML.
- Unrecognized `.env` keys warn at startup instead of refusing to boot.
- README config table now covers every setting.

### Fixed
- Long generations swap from the live stream to the finished file as soon as it lands, so the scrubber shows true duration and seeking works mid-run.
- Volume control state reconnected to the player.

### Removed
- Unused `ffmpeg` from all images (~600MB); audio encoding already runs through PyAV's bundled copy.
- Dead `pydub` dependency.
- Unreachable list form of `voice` from the speech parser and unused `VoiceCombineRequest` schema.
- Legacy Gradio UI (`ui/`) code cruft; superseded by the web player since ~v0.2.0
- Legacy ONNX config compose vars, endpoints e.g `/debug/session_pools`.
- `OUTPUT_DIR`, `OUTPUT_DIR_SIZE_LIMIT_MB`, `SAMPLE_RATE` settings, never read.

## [v0.7.2] 2026-08-06
### Security
- `fastapi>=0.128.8`, `starlette>=1.3.1` to close CVE-2025-62727 (quadratic `Range` header parsing in `FileResponse`, reachable through the audio download path) (#500).

### Changed
- CORS `allow_credentials` now defaults off. Starlette 1.x echoes the caller's origin with `allow-credentials: true` where 0.47 returned `*`; nothing here uses cookies or auth, so this keeps the prior behavior.
- Docker build cache moved from GHA to the GHCR registry so forks and local builds can pull it, plus uv cache mounts and reordered test-client layers (#501).
- `response_format` docs (correctly) now list `aac` as supported.

### Fixed
- FLAC and WAV no longer lose the tail end of the audio; better muxer header patching at finalize (#497, covers #448 and #463). Diagnosis by @Technologicat.

## [v0.7.1] - 2026-08-02
### Added
- `/v1/download/{filename}` takes an optional `?name=` save-as name (sanitized, stored extension kept) and sets it in `Content-Disposition`. Omitting it keeps the previous name.
- Web UI keyboard navigation and ARIA labeling across header, player controls, and editor.

### Changed
- `Content-Disposition` is now built by `FileResponse` rather than by hand, so the filename comes back quoted (`filename="x.mp3"`) instead of bare. The name itself is unchanged when `?name=` is omitted.
- Web UI restyle: better use of space, responsive down to slim widths, playbar pinned to the bottom on narrow viewports.
- Waveform slowed and softened, made framerate-independent, respects `prefers-reduced-motion`.
- README: AMD GPU (ROCm) troubleshooting, clarified docker-compose comments.

### Fixed
- Downloads save as `{voice}_{timestamp}.{format}`, not the temp name (#338). Covers right-click "Save audio as" too, since `Content-Disposition` outranks the link's `download` attribute.
- Aborted streams no longer surface as playback failures; a user-initiated `MEDIA_ERR_ABORTED` is told apart from a real error.
- Stream-to-file swap settles pending buffer operations instead of leaving the feeder awaiting forever.

## [v0.7.0] - 2026-07-31
### Added
- `AGENTS.md` contributor guidelines, plus `SKILL.md` notes for the API, benchmarks, and web areas.

### Changed / Optimizations
- Docker images build on Python 3.12 (project floor stays 3.10 for local installs). Rust dropped from the CPU builder.
- Runtime dependencies trimmed to remove deprecated imports
- bumped `requests`,`python-dotenv`, capped `transformers<6`
- Builds now explicitly require BuildKit (default since Docker 23, ~Jan 2023); utilizing `COPY --exclude`
- Model bake reworked to ensure weights land exactly once (whether prexisting or downloaded at build)
- ROCm image now bakes the model at build like CPU/GPU (instead of a first-run fetch)
- GPU runtime now only uses torch shipped cuDNN/etc via pip wheels (#482). (see table below for size changes)
- Transcription benchmark reports split by device; RTF and first-token baselines refreshed.

Compressed image sizes + new bases:
<div align="center">

| Image       |  v0.6.0  |  v0.7.0  | Runtime base                                        |
|:------------|---------:|---------:|:----------------------------------------------------|
| cpu         |  1.66 GB |  1.56 GB | `python:3.10-slim` -> `python:3.12-slim`             |
| gpu         |  6.81 GB |  4.68 GB | `cuda:12.6.3-cudnn-runtime` -> `cuda:12.6.3-base`    |
| gpu (cu128) |  8.11 GB |  5.23 GB | `cuda:12.8.1-cudnn-runtime` -> `cuda:12.8.1-base`    |
| rocm        | 13.08 GB | 13.36 GB | unchanged; model now baked in                        |

</div>

### Fixed
- Model validation checksums against downloaded release artifact to ensure consistency, downloads first to a temp dir to avoid clobbering pre-existing models in the case of network issues/corrupted downloads.
- Model validation also rejects any custom files under 100MB to avoids false pass results (e.g. a 9-byte "Not found"), allowing a re-download instead of passing (#301).
- `.dockerignore` Fixed pycache ignore pattern to `**/`  to ensure nested .pyc/etc stay out of build contexts.
- Removed dead `pydub` imports from the audio services.
- `_find_file` rejects lookups that escape its search roots (`../` sequences, absolute paths) to avoid unintentional exposure of files outside the voices/models/web dirs. Symlinks placed inside those dirs resolve as before.
- Text normalizer: anchored decimal regex to prevent quadratic backtracking on digit floods, reordered range substitution so `NUMBER_PATTERN` no longer swallows hyphens meant as range separators, added version-number handling (`2.0.1` renders as "two point zero point one" instead of being split).

## [v0.6.0] - 2026-07-12
### Breaking changes
- `POST /dev/unload` is off by default; set `ALLOW_DEV_UNLOAD=true` to enable, otherwise returns 403. Shipped open in v0.5.0, now opt-in (#483).
- `/debug/*` routes also set off by default, continuation of above; to avoid unintentional exposure of internals (stack traces, temp storage, CPU/mem/GPU); set `ENABLE_DEBUG_ENDPOINTS=true` to enable, otherwise 403's.
- Removed lingering deprecated `/debug/session_pools`

### Changed
- Documented API stability: `/v1/*` is the stable surface; `/dev/*` and `/debug/*` are operational helpers that may change or move behind flags between minor releases.

### Fixed
- OpenAI voice aliases pointed at legacy v0.19 voicepacks that sound degraded on the v1.0 model. Added the proper v1.0 `bf_isabella` and repointed `nova` (`bf_v0isabella` -> `bf_isabella`), `alloy`, `ash`, `coral`, `echo` to their v1.0 voices. The `v0*` voices stay available by explicit name. (#479)
- `/dev/captioned_speech` returned `timestamps: null` for non-English espeak voices (es/fr/it/hi/pt). Word timestamps are now derived from the model's own phoneme durations (`pred_dur`), so they match the audio exactly; falls back to the old behavior when word counts can't be reconciled. English path unchanged, ja/zh keep previous behavior. (#484)

## [v0.5.0] - 2026-06-06
### Added
- `POST /dev/unload` release model from VRAM without stopping container; lazy reload on next request. For freeing a shared GPU while idle. Reclaim scale with load (~0.7 GB; ~1.6 GB via long-form test on 4060Ti). (#474)
### Fixed
- Web UI long-playback bugfix around the 10-minute mark; in-browser audio buffer is now bounded ahead of `currentTime` with trailing eviction behind it, so long generations stop overflowing the SourceBuffer.
- Web UI stays responsive on extended sessions; waveform animation is transition-gated and `PlayerState` short-circuits no-op updates, so controls don't drift into lag after 10+ minutes of playback.
- Web UI MP3 seek/scrub works after stream completes; pausing or playback end auto-swaps to the full server file, allowing timeline navigation.

## [v0.4.0] - 2026-05-24
### Added
- GPU image variants for Blackwell / RTX 50-series (`:latest-cu128`, `:vX.Y.Z-cu128`, amd64 only) with PyTorch cu128 wheels (#443). Default `:latest` and new `:latest-cu126` alias stay on cu126 for Maxwell/Pascal compatibility.
- Integration test suite (`api/tests/integration/`, opt-in `integration` marker) and a `tts-api-test-client` image that round-trips speech through faster-whisper against a live server. Run via `docker/docker-compose.test.yml`.
- Web UI footer badge showing the server version from `/config`.

### Breaking changes
- `/v1/audio/voices` items in the `voices` array changed from plain strings to `{"id", "name"}` objects (#462) to match OpenWebUI/similar clients, and allow metadata in the response. Clients reading entries as strings will break; pass `?legacy=true` to restore the old item shape.
  - Old: `{"voices": ["af_heart", ...]}`
  - New: `{"voices": [{"id": "af_heart", "name": "af_heart"}, ...]}`

### Changed
- `api_version` now read from the `VERSION` file instead of hardcoded.
- Removed the legacy `docker/{cpu,gpu}/Dockerfile`; the `.optimized` variants are the only build files now.
- Docker images carry OCI metadata so GHCR pages render properly. Integration compose defaults to the published test-client image.
- ROCm image defaults to `MIOPEN_FIND_MODE=2` so the on-disk kernel cache is reused instead of re-searched per process, and ships an opt-in warmup script at `docker/rocm/warmup_miopen.py` to pre-populate it. Recipe and benchmarks from @realugbun in #454.

### Fixed
- WAV responses drop junk size-field trailer that decoded as a click at chunk end. (#463)
- ROCm MIOpen cache set to persist across compose restarts; switched bind mounts to named volumes at the path MIOpen writes to (prior mounts targeted an inaccessible location).
- cpu/gpu composes set `DOWNLOAD_MODEL=true` for an idempotent model fetch on startup.
- `VERSION` shipped into images so `/config` reports the real server version.
- Silence trimming no longer treats full-scale-negative samples as silent (`int16` `abs()` overflow).
- Fixed invalid escape sequences in the text-normalizer URL regex.
- CI test job uses the CPU PyTorch build and excludes integration tests by default.

## [v0.3.0] - 2026-05-15
### Added
- AMD GPU support via ROCm (`docker/rocm/` build, `rocm` extra in `pyproject.toml`). Also explored/proposed via @asheghi in #393.
- `gpt-4o-mini-tts` model alias for OpenAI-compatible clients.
- Reverse-proxy support for the Web UI (new `/config` endpoint exposing `UVICORN_ROOT_PATH`).
- Configurable logging level via the `API_LOG_LEVEL` environment variable.
- `INCLUDE_JAPANESE` Docker build flag for opt-in Japanese support.
- Transcription accuracy test harness under `examples/assorted_checks/test_transcription/` (baselines, multilingual reports, long-form runner).
- Override of `docker-bake.hcl` variables through GitHub Actions environment variables.

### Changed
- PyTorch bumped to 2.8.0 (x86_64: cu126, aarch64: cu129). x86_64 settled on cu126 to keep Maxwell/Pascal cards working, which drops native Blackwell (RTX 50-series) kernel support. Blackwell users need to override the torch index manually. See #443.
- `kokoro` bumped to 0.9.4 and `misaki` to 0.9.4 (proposed by @jcheek in #371, superceded).
- New optimized multi-stage Dockerfiles (`docker/{cpu,gpu}/Dockerfile.optimized`) become the default bake target. Reported image sizes: CPU 5.6 → 4.9 GB, GPU 14.8 → 9.9 GB.
- Parallelized Docker bake targets per architecture for faster CI.
- ROCBlas version pinned; ROCm docker-compose now builds locally.
- CI/release workflow hardening: pinned BuildKit/runners, branch-tagged builds, manifest fixes, `workflow_dispatch` ref and tag-check race fixed, `latest` tag gated.

### Fixed
- OGG/Opus audio truncation where the final page was lost during `write_chunk` finalize.
- Voice tensor loading hardened with `weights_only=True` (avoids unsafe pickle in `torch.load`).
- Per-request voice-tensor memory leak resolved via caching (#453), with cache cleared on unload.
- Custom phoneme handling made significantly more robust.
- Firefox Web UI playback falls back gracefully when `audio/mpeg` MSE is unsupported; waveform rendering bugfix bundled in the same web rewrite.
- CPU Docker builds: Rust now installed for `appuser` with proper `PATH` and longer `uv` timeouts.
- `cmake` added to CI deps to unblock `pyopenjtalk` builds (proposed by @jcheek in #371; superceded).
- `start-gpu.sh` uses `#!/usr/bin/env bash` for broader compatibility.
- Apple Silicon: `test_initial_state()` no longer fails.

## [v0.2.4] - 2025-06-18
### Added
- Apple Silicon (MPS) acceleration support for macOS users.
- Voice subtraction capability for creating unique voice effects.
- Windows PowerShell start scripts (`start-cpu.ps1`, `start-gpu.ps1`).
- Automatic model downloading integrated into all start scripts.
- Example Helm chart values for Azure AKS and Nvidia GPU Operator deployments.
- Volume multiplier setting.
- Chinese punctuation-based sentence splitting.
- `CONTRIBUTING.md` guidelines for developers.

### Changed
- Version bump of underlying Kokoro and Misaki libraries.
- Default API port reverted to 8880.
- Docker containers now run as a non-root user.
- Improved text normalization for numbers, currency, and time formats.
- Improved MP3 encoding and audio-pause handling.
- Updated and improved Helm chart configurations and documentation.
- Enhanced temporary file management with better error tracking.
- Web UI dependencies (Siriwave) are now served locally.
- Standardized environment variable handling across shell/PowerShell scripts.
- Rust installed in Dockerfile for builds requiring it.

### Fixed
- Download links no longer dropped when `streaming=false` and `return_download_link=true`.
- Windows PowerShell start scripts fixed around virtual-environment activation order.
- Potential segfaults during inference addressed.
- Helm chart issues around health checks, ingress, and default values.
- Audio-quality degradation from incorrect bitrate settings in some paths.
- Custom phonemes provided in input text are now preserved end-to-end.
- 'MediaSource' error affecting playback stability in the web player.
- CRLF line endings in `custom_responses.py` converted to LF.
- Money parsing and related tests.
- Additional safety checks on captioned-speech generation.
- Phoneme handling fixes.

### Removed
- Obsolete GitHub Actions build workflow; build and publish now occurs on merge to `Release` branch.

## [v0.2.3] - 2025-03-06
### Added
- Streaming word timestamps.
- `.gitattributes` for consistent line endings.

### Changed
- Text normalization improvements.

### Fixed
- Audio-quality regression caused by lower-bitrate encoding.
- Disabled uvicorn/FastAPI `--reload` to avoid pegging a CPU core.

## [v0.2.2] - 2025-02-13
### Added
- Helm chart.
- Settings-based override of the default `lang_code`.
- Advanced normalization settings.

### Fixed
- Speech not engaging reliably on the CPU image fallback.
- Audio quality bumped via adjusted compression settings.
- Web UI format-selection bug.

## [v0.2.1] - 2025-02-10
### Added
- Dummy `/v1/models` endpoint for OpenAI compatibility (#144).

### Changed
- Caption flow now streams audio with tempfile download at completion, removing duplicate captions (#139).

### Fixed
- Compatibility with the `espeak-loader` dependency on misaki (#127).
- Build system and model-download issues.

## [v0.2.0post1] - 2025-02-07
- Fix: Building Kokoro from source with adjustments, to avoid CUDA lock 
- Fixed ARM64 compatibility on Spacy dep to avoid emulation slowdown
- Added g++ for Japanese language support
- Temporarily disabled Vietnamese language support due to ARM64 compatibility issues

## [v0.2.0-pre] - 2025-02-06
### Added
- Complete Model Overhaul:
  - Upgraded to Kokoro v1.0 model architecture
  - Pre-installed multi-language support from Misaki:
    - English (en), Japanese (ja), Korean (ko),Chinese (zh), Vietnamese (vi)
  - All voice packs included for supported languages, along with the original versions.
- Enhanced Audio Generation Features:
  - Per-word timestamped caption generation
  - Phoneme-based audio generation capabilities
  - Detailed phoneme generation
- Web UI Improvements:
  - Improved voice mixing with weighted combinations
  - Text file upload support
  - Enhanced formatting and user interface
  - Cleaner UI (in progress)
  - Integration with https://github.com/hexgrad/kokoro and https://github.com/hexgrad/misaki packages

### Removed
- Deprecated support for Kokoro v0.19 model

### Changes
- Combine Voices endpoint now returns a .pt file, with generation combinations generated on the fly otherwise 


## [v0.1.4] - 2025-01-30
### Added
- Smart Chunking System:
  - New text_processor with smart_split for improved sentence boundary detection
  - Dynamically adjusts chunk sizes based on sentence structure, using phoneme/token information in an intial pass
  - Should avoid ever going over the 510 limit per chunk, while preserving natural cadence
- Web UI Added (To Be Replacing Gradio):
  - Integrated streaming with tempfile generation
  - Download links available in X-Download-Path header
  - Configurable cleanup triggers for temp files
- Debug Endpoints:
  - /debug/threads for thread information and stack traces
  - /debug/storage for temp file and output directory monitoring
  - /debug/system for system resource information
  - /debug/session_pools for ONNX/CUDA session status
- Automated Model Management:
  - Auto-download from releases page
  - Included download scripts for manual installation
  - Pre-packaged voice models in repository

### Changed
- Significant architectural improvements:
  - Multi-model architecture support
  - Enhanced concurrency handling
  - Improved streaming header management
  - Better resource/session pool management


## [v0.1.2] - 2025-01-23
### Structural Improvements
- Models can be manually download and placed in api/src/models, or use included script
- TTSGPU/TPSCPU/STTSService classes replaced with a ModelManager service
  - CPU/GPU of each of ONNX/PyTorch (Note: Only Pytorch GPU, and ONNX CPU/GPU have been tested)
  - Should be able to improve new models as they become available, or new architectures, in a more modular way
- Converted a number of internal processes to async handling to improve concurrency
- Improving separation of concerns towards plug-in and modular structure, making PR's and new features easier

### Web UI (test release)
- An integrated simple web UI has been added on the FastAPI server directly
  - This can be disabled via core/config.py or ENV variables if desired. 
  - Simplifies deployments, utility testing, aesthetics, etc 
  - Looking to deprecate/collaborate/hand off the Gradio UI


## [v0.1.0] - 2025-01-13
### Changed
- Major Docker improvements:
  - Baked model directly into Dockerfile for improved deployment reliability
  - Switched to uv for dependency management
  - Streamlined container builds and reduced image sizes
- Dependency Management:
  - Migrated from pip/poetry to uv for faster, more reliable package management
  - Added uv.lock for deterministic builds
  - Updated dependency resolution strategy

## [v0.0.5post1] - 2025-01-11
### Fixed
- Docker image tagging and versioning improvements (-gpu, -cpu, -ui)
- Minor vram management improvements
- Gradio bugfix causing crashes and errant warnings
- Updated GPU and UI container configurations

## [v0.0.5] - 2025-01-10
### Fixed
- Stabilized issues with images tagging and structures from v0.0.4
- Added automatic master to develop branch synchronization
- Improved release tagging and structures
- Initial CI/CD setup

## 2025-01-04
### Added
- ONNX Support:
  - Added single batch ONNX support for CPU inference
  - Roughly 0.4 RTF (2.4x real-time speed)

### Modified
- Code Refactoring:
  - Work on modularizing phonemizer and tokenizer into separate services
  - Incorporated these services into a dev endpoint
- Testing and Benchmarking:
  - Cleaned up benchmarking scripts
  - Cleaned up test scripts
  - Added auto-WAV validation scripts

## 2025-01-02
- Audio Format Support:
  - Added comprehensive audio format conversion support (mp3, wav, opus, flac)

## 2025-01-01
### Added
- Gradio Web Interface:
  - Added simple web UI utility for audio generation from input or txt file

### Modified
#### Configuration Changes
- Updated Docker configurations:
  - Changes to `Dockerfile`:
    - Improved layer caching by separating dependency and code layers
  - Updates to `docker-compose.yml` and `docker-compose.cpu.yml`:
    - Removed commit lock from model fetching to allow automatic model updates from HF
    - Added git index lock cleanup

#### API Changes
- Modified `api/src/main.py`
- Updated TTS service implementation in `api/src/services/tts.py`:
  - Added device management for better resource control:
    - Voices are now copied from model repository to api/src/voices directory for persistence
  - Refactored voice pack handling:
    - Removed static voice pack dictionary
    - On-demand voice loading from disk
  - Added model warm-up functionality:
    - Model now initializes with a dummy text generation
    - Uses default voice (af.pt) for warm-up
    - Model is ready for inference on first request
