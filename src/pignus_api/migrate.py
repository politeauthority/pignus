#!/usr/bin/env python

import json
import logging

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_debugtoolbar import DebugToolbarExtension


from pignus_api.models.user import User


def create_user():
    user = User()
    user.name = "alix"


if __name__ == "__main__":
    glow.db = db.connect()


# End File: pignus/src/pignus_api/migrate.py
