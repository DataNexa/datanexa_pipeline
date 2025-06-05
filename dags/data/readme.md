# Arquivos Temporários

## Estrutura
```bash
data/
│
├── raw/
│   ├── json/
|   |   ├── google/
│   |   ├── instagram/
│   |   ├── twitter/
│   |   └── youtube/
│   ├── html/
|   |   ├── google/
│   |   ├── instagram/
│   |   ├── twitter/
│   |   └── youtube/
│   |
├── processed/
|   ├── google/
│   ├── instagram/
│   ├── twitter/
│   └── youtube/
│
├── enriched/
│
└── ready/
```

Quem faz o gerenciamento é o `FileManager.py`