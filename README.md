# LowLevelKeyEvents

## Example usage

### config.json
```
{
    "classes": {
        "global": [
            {"key": 91, "action": "hold", "target": "win"}
        ],
        "win": [
            {"key": "1", "action": "switch", "target": "layer1"},  
            {"key": "2", "action": "switch", "target": "layer2"}
        ],
        "layer1": [
            {"key": "W", "action": "press", "target": "VK_UP"},
            {"key": "A", "action": "press", "target": "VK_LEFT"},
            {"key": "S", "action": "press", "target": "VK_DOWN"},
            {"key": "D", "action": "press", "target": "VK_RIGHT"},
            {"key": "O", "action": "shell", "target": "spotify.exe"},
            {"key": "P", "action": "press", "target": "0xB3"},
            {"key": "I", "action": "press", "target": "0xAF"},
            {"key": "K", "action": "press", "target": "0xAE"},
            {"key": "J", "action": "press", "target": "0xB1"},
            {"key": "L", "action": "press", "target": "0xB0"}
        ],
        "layer2": []
    },
    "enabled_classes": ["global"]
}
```

### Command line
`
python LLKE.py config.json
`
