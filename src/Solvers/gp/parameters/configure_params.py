import os


def configure_gp(conf_dict, run_key):
    """
    Add config to base param file
    - Format as dictkey = dictvalue
    - If key already in lines.split(" = "), replace the value
    """
    with open("parameters/base.params", "r") as f:
        lines = f.readlines()
    for key, value in conf_dict.items():
        for i, line in enumerate(lines):
            if key in line.split(" = "):
                lines[i] = f"{key} = {value}\n"
                print(f"Replaced {key} with {value}")

    os.mkdir("generated") if not os.path.exists("generated") else None
    conf_path = f"generated/config_{run_key}.params"

    with open(conf_path, "w") as f:
        f.writelines(lines)
    return os.path.join(os.getcwd(), conf_path)


def get_all_opts():
    """
    Get all options from base param file
    """
    with open("base.params", "r") as f:
        lines = f.readlines()
    opts = {}
    for line in lines:
        if " = " in line:
            key, value = line.split(" = ")
            opts[key] = value.strip()
    return opts


def pretty_print_options(opts):
    """
    Print options in a pretty way
    """
    for opt, val in opts.items():
        print(opt)







if __name__ == "__main__":
    conf_dict = {
        "evalthreads": 10,
    }
    pretty_print_options(get_all_opts())
    configure_gp(conf_dict, "test")

