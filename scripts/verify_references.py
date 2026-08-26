"""Verify the DOI metadata used in the Project Theta review against Crossref."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

DOIS = [
    "10.1038/s41583-022-00587-4",
    "10.1038/s41586-025-08888-1",
    "10.1016/j.neubiorev.2025.106053",
    "10.1038/s41562-021-01284-5",
    "10.1073/pnas.2116933119",
    "10.1080/17588928.2020.1772214",
    "10.1016/j.concog.2019.04.002",
    "10.1093/nc/niab001",
    "10.1093/nc/niab019",
    "10.1016/S0010-0277(00)00123-2",
    "10.1016/j.neuron.2020.01.026",
    "10.1073/pnas.95.24.14529",
    "10.1016/j.tics.2019.04.007",
    "10.1016/j.pneurobio.2020.101918",
    "10.1016/j.tics.2006.09.001",
    "10.1016/j.tics.2019.06.009",
    "10.1016/j.tics.2011.05.009",
    "10.3389/fnhum.2014.00443",
    "10.1093/nc/niz020",
    "10.1186/1471-2202-5-42",
    "10.1038/nrn.2016.44",
    "10.1371/journal.pcbi.1011465",
    "10.1093/nc/niy007",
    "10.1017/S0140525X21002387",
    "10.1016/j.tics.2013.09.007",
    "10.1038/nrn3950",
    "10.1016/j.tics.2018.08.008",
    "10.3389/fpsyg.2012.00096",
    "10.1016/j.crneur.2022.100036",
    "10.1016/j.biopsycho.2014.11.004",
    "10.3389/fpsyg.2015.00500",
    "10.1073/pnas.2102421118",
    "10.1016/j.pneurobio.2020.101844",
    "10.1016/j.tics.2015.10.002",
    "10.3389/fnhum.2022.861517",
    "10.1016/j.concog.2018.11.002",
    "10.1523/JNEUROSCI.0120-20.2020",
    "10.1126/science.aan8871",
    "10.1016/j.neunet.2013.03.011",
    "10.1016/j.concog.2007.04.005",
    "10.1016/j.tics.2025.10.011",
    "10.3389/frobt.2024.1437496",
    "10.1142/S270507852150003X",
]


def main() -> int:
    records = []
    errors = []
    for doi in DOIS:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ProjectThetaReview/1.0 (reference verification)"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                item = json.loads(response.read().decode("utf-8"))["message"]
            records.append({
                "doi": item.get("DOI"),
                "title": (item.get("title") or [""])[0],
                "authors": [
                    " ".join(part for part in (a.get("given"), a.get("family")) if part)
                    for a in item.get("author", [])
                ],
                "published": (item.get("published") or {}).get("date-parts"),
                "container": (item.get("container-title") or [""])[0],
                "volume": item.get("volume"),
                "issue": item.get("issue"),
                "pages": item.get("page"),
                "type": item.get("type"),
            })
        except Exception as exc:  # noqa: BLE001
            errors.append({"doi": doi, "error": f"{type(exc).__name__}: {exc}"})
        time.sleep(0.1)
    target = Path("research/reference-verification.json")
    target.write_text(
        json.dumps({"records": records, "errors": errors}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verified": len(records), "errors": errors, "output": str(target)}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
