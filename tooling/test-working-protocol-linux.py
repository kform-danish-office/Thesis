#!/usr/bin/env python3
"""Compatibility entrypoint for the now-portable production protocol runner."""
import runpy
runpy.run_path('/workspace/working-source/firmware/test_web_protocol.py', run_name='__main__')
