# Architecture des branches

## Orphelines

Chaque branche est **orpheline** — elles ne partagent aucun historique Git. Chacune contient uniquement les fichiers d'un langage et rien des autres. Cela évite toute contamination croisée et permet d'avoir des CI/CD, dépendances et outils propres à chaque langage sans se marcher dessus.

| Branche | Langage | Stack |
|---------|---------|-------|
| `main`  | TypeScript | React + Vite (frontend) + Node/Express (backend) |
| `python` | Python | Pygame |
| `rust` | Rust | macroquad |
| `go` | Go | Ebitengine |

Chaque branche doit pouvoir être clonée et exécutée de façon autonome sans dépendre d'une autre branche.

## Convention de worktree (dev local)

Pour travailler sur plusieurs branches simultanément sans `git stash` ni `git checkout` à chaque fois :

```
../ssht-main/     ← main (web TS/React)
../ssht-python/   ← python
../ssht-rust/     ← rust
../ssht-go/       ← go
```

Créer les worktrees :

```bash
git worktree add ../ssht-python python
git worktree add ../ssht-rust   rust
git worktree add ../ssht-go     go
```

Chaque worktree a son propre `node_modules/`, `target/`, etc. — pas de conflit.
