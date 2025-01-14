import argparse
import sys
from .core import generate_directory_tree
from .hierarchy import build_hierarchy
from .output import export_to_txt, export_to_json, export_to_docx, export_to_pdf_direct
from .config import load_config
import os

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Directory Structure Generation Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "root_dir",
        nargs='?',
        default=os.getcwd(),
        help="Root directory to generate the structure from."
    )

    parser.add_argument(
        "-o", "--output",
        default="directory_structure",
        help="Base name for the output files (without extension)."
    )

    parser.add_argument(
        "-c", "--config",
        help="Path to the configuration file (YAML or JSON)."
    )

    parser.add_argument(
        "-f", "--formats",
        nargs='+',
        choices=['txt', 'json', 'docx', 'pdf'],
        help="Output formats to generate.",
        default=["txt"]
    )

    parser.add_argument(
        "--hierarchy",
        action='store_true',
        help="Enable hierarchy parsing."
    )

    parser.add_argument(
        "-p", "--project-type",
        choices=['verilog', 'python', 'java', 'react', 'database', 'devops', 'ml', 'documentation', 'game'],
        help="Type of the project to determine hierarchy parsing.",
    )

    parser.add_argument(
        "--direct-pdf",
        action='store_true',
        help="Generate PDF directly from hierarchy without using a temporary text file."
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    config = load_config(args.config) if args.config else load_config()

    # Override config based on CLI arguments
    if args.formats:
        config['output_formats'] = args.formats

    if args.hierarchy:
        config['hierarchy']['enable'] = True

    if args.project_type:
        config['hierarchy']['project_type'] = args.project_type

    # Generate directory tree
    try:
        tree_lines, skipped_files, skipped_folders = generate_directory_tree(
            root_dir=args.root_dir,
            exclude_extensions=set(config.get("exclude_extensions", [])),
            exclude_folders=set(config.get("exclude_folders", []))
        )
    except Exception as e:
        print(f"Error generating directory tree: {e}")
        sys.exit(1)

    # Generate hierarchy if enabled
    if config['hierarchy']['enable']:
        project_type = config['hierarchy'].get('project_type', 'verilog')  # Default to verilog
        try:
            hierarchy = build_project_hierarchy(args.root_dir, project_type)
        except Exception as e:
            print(f"Error building hierarchy: {e}")
            hierarchy = {}
    else:
        hierarchy = {}

    # Export outputs
    if 'txt' in config['output_formats']:
        txt_output = f"{args.output}.txt"
        export_to_txt(tree_lines, skipped_files, skipped_folders, txt_output, hierarchy if config['hierarchy']['enable'] else None)
        print(f"Exported directory structure to {txt_output}")

    if 'json' in config['output_formats']:
        if config['hierarchy']['enable']:
            tree_hierarchy = hierarchy
        else:
            tree_hierarchy = build_hierarchy(args.root_dir)
        json_output = f"{args.output}.json"
        export_to_json(tree_hierarchy, json_output)
        print(f"Exported directory hierarchy to {json_output}")

    if 'docx' in config['output_formats']:
        docx_output = f"{args.output}.docx"
        export_to_docx(tree_lines, skipped_files, skipped_folders, docx_output, hierarchy if config['hierarchy']['enable'] else None)
        print(f"Exported directory structure to {docx_output}")

    if 'pdf' in config['output_formats']:
        if args.direct_pdf and config['hierarchy']['enable']:
            pdf_output = f"{args.output}.pdf"
            export_to_pdf_direct(hierarchy, pdf_output)
            print(f"Exported directory structure to {pdf_output}")
        else:
            txt_temp = f"{args.output}_temp.txt"
            export_to_txt(tree_lines, skipped_files, skipped_folders, txt_temp, hierarchy if config['hierarchy']['enable'] else None)
            pdf_output = f"{args.output}.pdf"
            export_to_pdf(txt_temp, pdf_output)
            os.remove(txt_temp)
            print(f"Exported directory structure to {pdf_output}")

    # Handle hierarchy JSON if needed
    if config['hierarchy']['enable']:
        hierarchy_output = f"{args.output}_hierarchy.json"
        export_to_json(hierarchy, hierarchy_output)
        print(f"Exported directory hierarchy to {hierarchy_output}")

if __name__ == "__main__":
    main()
