#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:40:23 2016

@author: mittelberger
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('user')

args = parser.parse_args()

print(args.user)
