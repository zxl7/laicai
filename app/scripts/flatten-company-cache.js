import fs from "fs";
import path from "path";

function flattenCompany(company) {
  const result = {};
  if (company && typeof company === "object") {
    if (company.code !== undefined) result.code = company.code;
    if (company.lastUpdated !== undefined) result.lastUpdated = company.lastUpdated;
    const list = company.list && typeof company.list === "object" ? company.list : null;
    if (list) {
      for (const k of Object.keys(list)) {
        if (!(k in result) && !(k in company)) result[k] = list[k];
        else if (!(k in result)) result[k] = list[k];
      }
      result.list = list;
    }
    for (const k of Object.keys(company)) {
      if (k === "list") continue;
      if (!(k in result)) result[k] = company[k];
    }
  }
  return result;
}

function main() {
  const inputArg = process.argv[2] || path.join("public", "company-cache.json");
  const inputPath = path.isAbsolute(inputArg) ? inputArg : path.join(process.cwd(), inputArg);
  if (!fs.existsSync(inputPath)) {
    console.error("File not found:", inputPath);
    process.exit(1);
  }
  const raw = fs.readFileSync(inputPath, "utf8");
  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    console.error("Invalid JSON:", e.message);
    process.exit(1);
  }
  if (!data || typeof data !== "object") {
    console.error("Unexpected JSON root type");
    process.exit(1);
  }
  const backupPath = inputPath.replace(/\.json$/i, ".backup.json");
  fs.writeFileSync(backupPath, JSON.stringify(data, null, 2));
  const out = {};
  for (const key of Object.keys(data)) {
    out[key] = flattenCompany(data[key]);
  }
  fs.writeFileSync(inputPath, JSON.stringify(out, null, 2));
  console.log("Updated:", inputPath);
  if (out["300377"]) {
    const sampleKeys = Object.keys(out["300377"]).slice(0, 20);
    console.log("Sample 300377 keys:", sampleKeys.join(", "));
    console.log("Has dm at top-level:", Object.prototype.hasOwnProperty.call(out["300377"], "dm"));
  }
}

main();
