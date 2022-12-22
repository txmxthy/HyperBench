```
{
  "name" : "instance", // the name of the instance [required]
  "jobs" : n,          // the number of jobs [required]
  "machines" : m,      // the number of machines [required]
  "optimum" : c,       // the optimum makespan or null [required]
  "bounds" : {         // required when the optimum is null
    "upper" : ub,      // the upper-bounds of makespan
    "lower" : lb,      // the lower-bounds of makespan
  },
  "path" : "*****"     // the file path to the instance [required]
}
```