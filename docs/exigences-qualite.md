# Exigences de qualité

## Applicables à toutes les branches

1. **Zéro erreur** du compilateur / type checker avant tout commit.
2. **Zéro warning** du linter.
3. **Les tests passent** avant de créer une PR.
4. **Noms en anglais** dans le code (variables, fonctions, fichiers). Les commentaires et la doc peuvent être en français.
5. **Pas de code mort** : pas de variable/import/fonction déclaré·e et jamais utilisé·e.
6. **Suivre les conventions** du langage et du framework déjà en place dans le projet.

## Par langage

| Branche | Linter | Type check | Build | Tests |
|---------|--------|------------|-------|-------|
| `main` | ESLint | `tsc --noEmit` | Vite | — |
| `python` | Ruff | Pyright | — | — |
| `rust` | Clippy | — | `cargo build` | `cargo test` |
| `go` | golangci-lint | — | `go build ./...` | `go test ./...` |

## Scripts de vérification

Chaque branche fournit une commande `check` qui regroupe lint + typecheck + build + tests :

```bash
make check   # lance tout
```
