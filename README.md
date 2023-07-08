#  PDK installation for Klayout

Explains how to install PDKs for klayout tool.


## **Usage**

To install requirements, you need to run the following command:

```bash
    pip install -r requirements.txt
```

To install PDK for klayout tool, you need to run the following command:

```bash
    install_tech.py (--help| -h)
    install_tech.py (--tech_name=<tech_name>) (--tech_path=<tech_path>)
```

Example:

```bash
    python3 install_tech.py --tech_name=sky130A --tech_path=$PDK_ROOT/$PDK/libs.tech/klayout
```
