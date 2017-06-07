# Handling perf issues - Exercices

## ex1

Based on the openacademy module, this exercice is quite simple.

Restore the dump ex1.dump to work
```
$ createdb ex1
$ pg_restore -d ex1 ex1.dump
```

Launch odoo with something like:
```
$ ./odoo-bin --addons-path=./addons,../technical-training/98-perf-issues/ex1 --db-filter=^ex1$ -d ex1 -i ex1_mod
```

### Symptom

* Quite impossible to display a session
* It's way too slow to delete a partner even without any session
* Searching on sessions is not optimal
* Displaying the list of the courses is not optimal
