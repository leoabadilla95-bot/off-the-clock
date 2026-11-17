// node gen_krea.mjs [epFrom] [epTo] — generate every unfinished job in ../img/jobs.json with Krea, 4 at a time.
import { Krea } from "@krea-ai/sdk";
import { readFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const S = join(dirname(fileURLToPath(import.meta.url)), "..");
const [lo, hi] = [Number(process.argv[2] ?? 1), Number(process.argv[3] ?? 10)];
const krea = new Krea({ apiKey: process.env.KREA_API_KEY });
const todo = JSON.parse(readFileSync(join(S, "img", "jobs.json"), "utf8"))
  .filter(j => j.ep >= lo && j.ep <= hi && !existsSync(join(S, "img", "done", j.id + ".json")));
console.log("todo", todo.length);

let failures = 0;
async function one(j) {
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const r = await krea.subscribe("image/krea/krea-2/medium", {
        input: { prompt: j.prompt, aspect_ratio: j.w > j.h ? "16:9" : "9:16", resolution: "1K" },
      });
      const url = r.data?.urls?.[0];
      if (!url) throw new Error("no url: " + JSON.stringify(r).slice(0, 300));
      console.log(execFileSync("python", [join(S, "dl.py"), j.id, url]).toString().trim());
      return;
    } catch (e) {
      console.log("fail", j.id, attempt, String(e).slice(0, 300));
      if (/credit|quota|insufficient|balance|401|403/i.test(String(e))) throw e;
    }
  }
  failures++;
}
const queue = todo.slice(0, Number(process.env.LIMIT || 1e9));
await Promise.all([1, 2, 3, 4].map(async () => { while (queue.length) await one(queue.shift()); }));
console.log("finished, failures:", failures);
