from __future__ import annotations

import hashlib
import sys


def file_sha256(path: str) -> str | None:
    sha256_hash = hashlib.sha256()
    try:
        with open(path, 'rb') as file:
            for chunk in iter(lambda: file.read(1024 * 1024 * 10), b''):
                sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f'file not found: {path}', file=sys.stderr)
    except Exception as e:
        print(f'error, e = {e}')
    return None
