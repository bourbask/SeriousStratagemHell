# Process de livraison

## Principe

Toutes les branches sont protégées sur GitHub. Aucun push direct n'est autorisé. Toute modification passe obligatoirement par une Pull Request.

## Workflow

1. **Créer une branche de travail** depuis la branche cible :
   ```bash
   git checkout main
   git checkout -b ma-feature
   ```

2. **Développer**, commit, push :
   ```bash
   git add -A
   git commit -m "feat: description"
   git push origin ma-feature
   ```

3. **Créer la Pull Request** (via `gh` ou GitHub UI) :
   ```bash
   gh pr create --base main --head ma-feature --title "feat: ..." --body ""
   ```

4. **Merge** (squash, admin bypass car mêmes développeur·se·s) :
   ```bash
   gh pr merge <num> --squash --admin --subject "feat: ..."
   ```

5. **Nettoyer** :
   ```bash
   git checkout main && git pull origin main
   git branch -d ma-feature
   git push origin --delete ma-feature
   ```

## Règles

- Toujours `git pull origin <cible>` avant de créer une branche de travail.
- Ne **jamais** faire de `git rebase` — toujours merger (`git pull origin <cible>`, pas `rebase`).
- Le message de commit ne doit contenir **aucune** mention d'IA (ni `Co-Authored-By: Claude`, ni `🤖`, ni `Generated with ...`).
- Les commits locaux sont signés sans GPG (`git commit --no-gpg-sign`).
- Supprimer la branche de travail après merge (locale ET distante).
