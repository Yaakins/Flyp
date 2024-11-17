# Flyp

## What is Flyp?

 Flyp is a programming language and a compiler made in plain c
 without external dependencies (such as LLVM).
 It is at its beginning, and still under development, so
 it's acquiring slowly more and more features.
 I'm doing this project in an educational purpose, 
 and I am aware that nothing is optimal neither clean code.
 My objective is to make something I'm happy with, and to learn
 how compilers work.

## Building

 I've only testd building with gcc 13.2.0 with Ubuntu, and cannot
 confirm how it would react under other conditions. Since it only
 requires standard gnu libc, it shouldn't face major problems 
 to build as soon as you don't use any exotic operating system.

 To build, simply execute `make` in the root directory,
 and the flyp executable will be output in `./build`
