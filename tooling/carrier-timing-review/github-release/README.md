# Published GitHub PWR-2.0.4 V2 pre-release

Published2026-10-25: https://github.com/kform-danish-office/Thesis/releases/tag/pwr-2.0.4
Release423166048, draft=false, prerelease=true. This is V2/STM32F410CBU6 only; physical bench validation remains pending. No board was flashed.

All five assets were uploaded after user-approved standard GitHub CLI device authentication. Initial platform-authentication mismatch at uploads.github.com was resolved through that supported sign-in; no proxy credential was retrieved. Credentials remain in temporary CLI configuration outside the workspace and are not included in snapshots or uploaded assets. Authentication/processes must not be assumed to survive a new task.

Assets: the F410 HEX, public release ZIP with instructions/protocol/port notes, matching firmware source ZIP, build metadata JSON and outer SHA256SUMS. All were downloaded from the GitHub draft and matched staged bytes, sizes, hashes and ZIP CRCs. After publication all five server digests/IDs/sizes remained correct and the HEX also downloaded anonymously from its public URL with the expectedSHA256. Metadata is in published-release.json and release-state.json; manifests/checks are asset-manifest.json and draft-download-verification.json.

The release tag points to existing baseline e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a. No new Git commit or branch update was performed. main and /workspace/Thesis remain clean at that baseline. The release body and source README explicitly identify pwr-2.0.4-v2-source.zip as canonical for the actual2.0.4 build; automatic GitHub Source code archives contain the older baseline. The attached source carries exact firmware/build/test code and adapted publication documentation with SOURCE-SHA256SUMS. Both native suites passed from that packaged source; only the F410 HEX is shipped. The source ZIP excludes generated harnesses, binary build products, thesis/photos/workbooks/private bench data, skills and credentials.

The initial private ZIP remains unchanged at the previous path. Public packages are separately named and have their own verified hashes. Local source documentation now records the verified pre-release link; the firmware/build/test code itself is unchanged and the original import archives/manifests are retained. Current source manifest and setup report have been updated. No hardware actions, sharing changes or environment publication occurred.

Final read-only artifact review found no publication blocker. One minor binary-package port-note link refers to the linker file available in the separate source ZIP rather than in the binary ZIP; the source bundle and release instructions identify the correct file. No asset was changed after its upload/hash verification.
