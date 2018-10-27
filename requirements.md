# Sample requirements — personal notes app

## Functional

- [x] F1: User can create a note with title and body
- [x] F2: User can list all notes
- [ ] F3: User can search notes by keyword
- [ ] F4: User can tag notes and filter by tag
- [x] F5: User can delete a note

## Non-functional

- [ ] NF1: List endpoint responds in under 200ms at p95 for 10k notes
- [x] NF2: Passwords stored with a slow hash (bcrypt/argon2)
- [ ] NF3: TLS required in production
- [ ] NF4: Daily automated backups of the datastore
