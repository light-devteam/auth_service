from collections import deque
from typing import Any
import json


def validate_raw_json(
    value: dict[str, Any],
    max_size_bytes: int = 2048,  # 2 KB
    max_top_level_keys: int = 20,
    max_depth: int = 10,
) -> dict[str, Any]:
    config_json = json.dumps(value)
    config_bytes = len(config_json.encode('utf8'))
    if config_bytes > max_size_bytes:
        raise ValueError(f'JSON too large: {config_bytes} bytes (max {max_size_bytes})')
    if len(value) > max_top_level_keys:
        raise ValueError(f'Too many top-level keys: {len(value)} (max {max_top_level_keys})')

    def check_depth(obj: dict | list, max_depth: int) -> int:
        if not isinstance(obj, (dict, list)):
            return 0
        depth = 0
        q = deque([(obj, 1)])
        while q:
            node, node_depth = q.popleft()
            depth = max(depth, node_depth)
            if depth > max_depth:
                raise ValueError(f'Max depth ({max_depth}) exceeded')
            if isinstance(node, dict):
                for v in node.values():
                    if isinstance(v, (dict, list)):
                        q.append((v, node_depth + 1))
            elif isinstance(node, list):
                for item in node:
                    if isinstance(item, (dict, list)):
                        q.append((item, node_depth + 1))
        return depth

    check_depth(value, max_depth)
    return value
