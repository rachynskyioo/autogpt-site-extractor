from autogpt.main import run_auto_gpt
from argparse import ArgumentParser
import ruamel.yaml as yaml
import os


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--openai_key', dest='openai_key', type=str, help='OpenAI API key')
    parser.add_argument('--link', dest='link', type=str, help='link for company web-site')
    parser.add_argument('--framework_type', dest='framework_type', type=str, choices=["babyAGI", "autoGPT"],
                        default="autoGPT", help='autoGPT or babyAGI')
    opts = parser.parse_args()
    return opts.openai_key, opts.link, opts.framework_type


def build_config(config_name, site_link=None):
    with open(config_name, "r") as file:
        conf = yaml.safe_load(file)
        conf['ai_goals'] = [goal.format(link=site_link) for goal in conf.get("ai_goals", [])]
        return conf


if __name__ == '__main__':
    key, site_link, framework_type = parse_args()
    config_name = "babyagi_config.yaml" if framework_type == "babyAGI" else "autogpt_config.yaml"
    config = build_config(config_name, site_link)
    os.environ["OPENAI_API_KEY"] = key
    try:
        print(f"MY CONFIG: {config}")
        run_auto_gpt(**config)
    finally:
        os.environ["OPENAI_API_KEY"] = ""
