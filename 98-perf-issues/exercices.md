# Handling perf issues - Exercices

## ex0

* Adjust log level to see time taken by an rpc request in the odoo logs
* Log all postgresql queries which takes more than 75 milliseconds to be handled in a csv log.
* Analyse the log with PgBadger

Those steps are quite mandatory for the next exercices

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

## ex2

Based on a standard Odoo v10.0 enterprise with l10n_be, no custom code, this script have issues after having created some entries.


Launch Odoo with something like 
```
./odoo-bin -d ex2 -i l10n_be
```

### Symptom

* The entries takes more and more time to be created
