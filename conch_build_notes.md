# The conch: build notes

This file lives on ELEMENTS so the build never depends on a chat session's memory.
Fable 5.2 writes here at every step. Times are this Mac's clock (Eastern).

## Where it stands

2026-11-17 02:40
- The conch was written in Fable's cloud workspace between 02:06 and 02:21 tonight and
  had not been written to this drive. Everett, 02:25: "It needs to be written on the
  elements volume" and saved every 5 minutes.
- From 02:35 on, this folder is the only place the conch is written. Nothing is staged
  anywhere else first.
- Being written here now: eleven files, 2,776 lines.
- Tests in the cloud copy: 55 run, 54 pass, 1 fails
  (test_every_line_has_its_clock_and_its_kind). Not yet run on this Mac.

## The eleven files and their fingerprints

sha256 of the cloud copy at 02:33. A file has landed whole when
`shasum -a 256 <file>` in this folder gives the same line.

    7be2c52bce86bc8f75dbaf52b3ea913f3677fdf656378dab811a5cd10fc515f8  conch.py
    4364854aabbfcc61368a7bce2d31348c9f54b0d74b3182bac23d84ae275f053c  conch_bench.py
    0323087c166f85db6df5671eb670cd7f55f615eabb76e312b158fd894fa06ca5  conch_fold.py
    43f862634dbf5199e7fc78784bccc201fe54748235b620531975e67286d0e020  conch_intake.py
    61bf4ebb77583fe41e882e017643695bc078d2201fe157e8aed61b500b3923e1  conch_level3.py
    a6b483629a040d63f1c3c7ad3ecc17fe440e66b3a2528a11d8026e108c21d3e4  conch_lip.py
    24f512134a353da107f5afb12211e127a2760071db72000c413e957dc8c7ab3c  conch_open.py
    e0f76060a480f10aa60b194baa4bffbf9a74554d0d04c00eef7ef8c06633a5c5  conch_records.py
    9ff7c37dbc2335499650b3c746f568637e0d09c55a2ca78296fae80639635bb2  conch_sleep.py
    52c366843f6272cd63723ef8924abb1762c7312b0a435219b0d80286973cac38  conch_spiral.py
    6549412551fa6c051184fb5d3bd6bba15a801bc0e68682e79af46b843936693b  test_conch.py

## Check it yourself

    cd /Volumes/ELEMENTS/3C
    shasum -a 256 conch*.py test_conch.py
    /usr/bin/python3 -m unittest test_conch          # the Mac's own Python 3.9
    /usr/local/bin/python3 -m unittest test_conch    # Python 3.13

## If the session restarts (for Fable)

1. Read this file before anything else. Do not rebuild from memory.
2. Run the shasum line above and compare with the fingerprints.
3. A file that is missing or different still has to come across. The cloud copy is in
   the same session at
   /tmp/claude-0/-home-claude/5c97380b-d12f-59e0-ab65-bb0ba7b96abe/scratchpad/conch_build/
   and a zip of it was sent to Everett in the chat at 02:37.
4. Once all eleven match, this drive is the only source. Edit here, test here.
