# Negative Knowledge: Fixed RLIMIT_AS in 64-bit Ruby

## Context
When running untrusted code in a sandboxed child process (`Process.fork`), we wanted to limit memory usage using `Process.setrlimit(Process::RLIMIT_AS, bytes)`.

## What Was Tried
Setting a fixed limit like `128 * 1024 * 1024` (128MB) directly in the child process.

## Why It Failed
In 64-bit Linux with glibc, Ruby's baseline virtual address space (VSZ) upon initial fork and library mapping is already ~450MB. Setting `RLIMIT_AS` to 128MB caused the child process to immediately fail with memory allocation errors on any malloc, even for a simple integer calculation.

## Anti-Pattern Rule
**DO NOT** assign a small, fixed virtual memory size to `RLIMIT_AS`. Always calculate allowable growth dynamically based on baseline VSZ:
```ruby
base_vsz = (File.read("/proc/self/statm").split[0].to_i * 4096) rescue (512 * 1024 * 1024)
mem_bytes = base_vsz + (allowable_growth_mb * 1024 * 1024)
```
