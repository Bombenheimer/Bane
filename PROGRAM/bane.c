/*
* MIT License
* 
* Copyright (c) 2024 Bombenheimer
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*/

// DEFINE MACRO FOR GNU SOURCE
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

// ADD LIBRARIES FOR WINDOWS
#ifdef _WIN32
#include <curses.h>
#endif

// ADD LIBRARIES FOR UNIX AND LINUX
#if defined(__linux__) && defined(__APPLE__) && defined(__MACH__)
#include <curl.h>
#include <ncurses.h>
#endif

// STANDARD LIBRARIES
#include <stdio.h>

int main(int argc, char* argv[])
{
  return 0;
}
