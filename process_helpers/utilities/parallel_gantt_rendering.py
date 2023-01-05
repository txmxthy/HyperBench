import os
from multiprocessing import Pool
from tqdm.auto import tqdm
from process_helpers.utilities.plotting import render_gantt_json


def use_args(x):
    alg_path = x[0]
    idn = x[1]
    json_file = x[2]
    dataset = x[3]

    img_path = f"{alg_path}\\results\\gif\\img\\{dataset}\\"
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    render_gantt_json(infile=json_file, destination=img_path)


def make_parallel_args(algs, datasets, root_path, json_root, encoding):
    print(f"Algs {algs}, Datasets {datasets}, Root {root_path}, JSON {json_root}")
    print(f"Encoding {encoding}")

    args = []
    decode_key = {}
    for alg in algs:
        if alg in encoding:
            # Slurm -> Dataset is 1:Many for dispatching
            print(f"Alg {alg} has encoding {encoding[alg]}")
            decode_key = encoding[alg]
        alg_path = f'{root_path}\\output\\{alg}'

        json_path = f"{json_root}{alg}\\json\\"

        unique_id_file = f"{alg_path}\\unique_solution_ids.txt"
        print(f"Reading {unique_id_file}")
        with open(unique_id_file, "r") as f:
            for identifier in f.read().splitlines():
                # Different batching as they run fast and share writer - json is prefixed with dataset
                results_file = f"{root_path}results_sorted_{alg}.csv"
                with open(results_file, 'r', encoding='utf_8_sig') as csvfile:
                    dataset_name = next(
                        (row.split(",")[0] for row in csvfile if identifier == row.split(",")[-1].rstrip()), None)

                    # If encoding keys has alg name, then we need to decode the dataset name:
                    if alg in encoding:
                        # Slurm -> Dataset is 1:Many for dispatching
                        print(f"Alg {alg} has encoding {encoding[alg]}")
                        # Take the first 3 characters of the identifier and lookup in decode key

                        encoded_dataset = identifier[:3]
                        print(identifier)
                        print(f"Encoded dataset {encoded_dataset}")
                        dataset_name = decode_key[encoded_dataset]
                        identifier = identifier[3:]

                        print(f"Decoded {dataset_name} from {identifier}")
                        input("Press Enter to continue...")
                    if alg == "dispatching_rules" or alg == "constraint":
                        json_file = f"{json_path}{dataset_name}-{identifier}_gantt.json"
                    else:
                        json_file = f"{json_path}{identifier}_gantt.json"

                args.append((alg_path, identifier, json_file, dataset_name))
    return args


def render_parallel_gantt(args):
    pool = Pool(processes=6)
    r = list(tqdm(pool.imap(use_args, args), total=len(args)))


if __name__ == '__main__':
    pass
    # print("Rendering Gantt Charts")
    # datasets = ["abz5"]
    # algs = ["genetic"]
    # root_path = "/home/kali/PycharmProjects/Capstone/jobs/"
    # render_gantt_in_parallel(algs, datasets, root_path)
