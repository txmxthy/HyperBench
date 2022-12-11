//
// Created by kwh44 on 12/7/18.
//

#ifndef HYBRID_ALGORITHM_SCHEDULE_H
#define HYBRID_ALGORITHM_SCHEDULE_H

#include <string>
#include "Chromosome.h"
#include "Operation.h"
#include <iostream>

class Schedule {
private:
    size_t number_of_jobs;
    size_t number_of_operations_in_one_job;
    std::vector<Operation> operations;
    std::vector<int> array_of_finish_times;
    // Arrays of scheduled operations contains indexes of elements in vector operations
    std::vector<int> array_of_scheduled_operations;
public:

    Schedule() = default;

    explicit Schedule(std::vector<std::vector<int> > &data_set);

    Schedule &operator=(const Schedule &) = default;

    Schedule &operator=(Schedule &&) noexcept = default;

    int cost_function(Chromosome &, bool);

    std::vector<int> &get_array_of_finish_times() { return array_of_finish_times; }

    std::vector<int> &get_array_of_scheduled_operations() { return array_of_scheduled_operations; }

private:
    void construct_schedule(Chromosome &);

    void update_E(std::vector<int> &, std::vector<int> &, std::vector<int> &, int, int, Chromosome &);

    int get_highest_priority_operation(std::vector<int> &, Chromosome &);

    static int time_of_g_iteration(std::vector<int> &, int);

    void local_search(Chromosome &);

    std::vector<int> get_critical_blocks(std::vector<int> &);

    int precedence_capacity_earliest_finish_time(int, std::vector<int> &, std::vector<int> &, Chromosome &);

    std::vector<int> find_critical_path(std::vector<int> &, std::vector<int> &);

    bool evaluate_swap(Chromosome &, std::vector<int> &, std::vector<int> &, int, int);

    void _new_ef(std::vector<int> &, std::vector<int> &, int, Chromosome &);
};

#endif //HYBRID_ALGORITHM_SCHEDULE_H
