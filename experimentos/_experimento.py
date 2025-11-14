from time import time
from typing import Dict, Iterable, List, Optional, Tuple, Union
import os
import json
import random
import math

from aima.search import hill_climbing, simulated_annealing, exp_schedule

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from problem_exp import GasProblem
from state_exp import generate_initial_state_empty, generate_initial_state_random, generate_initial_state_greedy

from Practica_ABIA.problem_parameters import ProblemParameters


class Experimento:
    def __init__(self, numero_repeticiones: int = 10, out_dir: str = "resultados", seed: Optional[int] = None):
        self.n = int(numero_repeticiones)
        self.cache = dict()  # idx -> (variant_name, (times_list, values_list_of_tuples))
        self.rows = []       # long-form rows for CSV
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        self.global_seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.operators = 0


    def sa_run_with_trace(
        self,
        problem,
        schedule_params: Optional[Tuple[float, float, int]] = None,
        label: Optional[str] = None,
        seed: Optional[int] = None
    ) -> dict:
        """
        Runs aima.simulated_annealing and returns the per-accepted-move trace stored in the state.
        The trace is a list of (beneficio, distancia+perdida) tuples. Length = accepted moves + 1.
        """
        if schedule_params is not None:
            k, lam, limit = schedule_params
        else:
            k, lam, limit = (20.0, 0.005, 100)
        # reset initial state's counters/trace
        problem.initial.pasos = 0
        problem.initial.sa_trace = [
            (float(problem.initial.beneficio), float(problem.initial.distancia + problem.initial.perdida_no_asignadas))
        ]
        schedule = exp_schedule(k, lam, limit)
        def safe_schedule(t, _s=schedule):
            T = _s(t)
            return 1e-12 if T <= 0 else T
        t1 = time()
        state = simulated_annealing(problem, schedule=schedule)
        t2 = time()
        return {
            "label": label or "SA-trace",
            "schedule": (float(k), float(lam), int(limit)),
            "trace": list(getattr(state, "sa_trace", [])),
            "accepted_ratio": (len(getattr(state, "sa_trace", [])) - 1) / float(limit) if limit else 0.0,
            "final_state": state
        }

    def plot_sa_trace_beneficio_coste(
        self,
        traces: List[dict],
        filename: str = "sa_trace_beneficio_coste.png",
        title: Optional[str] = None
    ) -> str:
        """
        Plots beneficio and (distancia + perdida) vs pasos for one or multiple traces.

        Input traces: list of dicts as returned by sa_run_with_trace (uses .trace and .label).
        Produces a 2-row plot:
          - Top: beneficio vs pasos.
          - Bottom: (distancia + perdida) vs pasos.
        """
        plt.figure(figsize=(10, 7))
        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2, sharex=ax1)

        for tr in traces:
            label = tr.get("label", "trace")
            data = tr["trace"]
            pasos = list(range(len(data)))
            beneficio = [b for (b, c) in data]
            coste = [c for (b, c) in data]  # distancia + perdida

            ax1.plot(pasos, beneficio, label=f"{label} | beneficio")
            ax2.plot(pasos, coste, label=f"{label} | dist+perd")

        ax1.set_ylabel("Beneficio")
        ax1.set_title(title or "SA: Beneficio y (Distancia + Pérdida) vs Pasos")
        ax1.grid(True, alpha=0.25)
        ax1.legend(loc="best", fontsize=8)

        ax2.set_xlabel("Pasos")
        ax2.set_ylabel("Distancia + Pérdida")
        ax2.grid(True, alpha=0.25)
        ax2.legend(loc="best", fontsize=8)

        plt.tight_layout()
        out = os.path.join(self.out_dir, filename)
        plt.savefig(out, dpi=150)
        plt.close()
        return out

    # ---------- Low-level runners ----------

    def experimento_hc(self, problem, label: str, multiplicador:int,initial_state:Optional[str] = None, reps:int = 10) -> Tuple[List[float], List[Tuple[float, float]]]:
        if initial_state is None:
            initial_state = "Not relevant"
        times_problem: List[float] = []
        vals_problem: List[Tuple[float, float]] = []
        for i in range(reps):
            print(f"Repeticion {i}")
            t0 = time()
            state = hill_climbing(problem)
            t1 = time()
            times_problem.append(t1 - t0)
            vals_problem.append((state.beneficio, state.distancia))
            # Store row for CSV
            self.rows.append({
                "variant": label,
                "algorithm": "HC",
                "initial_state":initial_state,
                "run": i,
                "multiplicador":multiplicador, 
                "beneficio": float(state.beneficio),
                "distancia": float(state.distancia),
                "pasos": state.pasos,
                "peticiones_satisfechas": sum([1 for gas in state.current_state for pet in gas if pet is not None]),
                "time_sec": round(t1 - t0, 4),
                "schedule_k": None,
                "schedule_lambda": None,
                "schedule_limit": None,
                "seed": self.global_seed
            })
        return times_problem, vals_problem

    def experimento_sa(self, problem, label: str, schedule_params: Optional[Tuple[float, float, int]], multiplicador:int,
                       initial_state:Optional[str] = None, reps:int = 10) -> Tuple[List[float], List[Tuple[float, float]]]:
        if initial_state is None:
            initial_state = "Not relevant"

        if schedule_params is not None:
            k, lam, limit = schedule_params
        else:
            k, lam, limit = (20, 0.005, 100)
        schedule = exp_schedule(k, lam, limit)

        times_problem: List[float] = []
        vals_problem: List[Tuple[float, float]] = []
        for i in range(reps):
            print("Repeticion", i)
            t0 = time()
            state = simulated_annealing(problem, schedule=schedule)
            t1 = time()
            times_problem.append(t1 - t0)
            vals_problem.append((state.beneficio, state.distancia))
            # Store row for CSV
            self.rows.append({
                "variant": label,
                "algorithm": "SA",
                "initial_state": initial_state,
                "run": i,
                "multiplicador":multiplicador,
                "beneficio": float(state.beneficio),
                "distancia": float(state.distancia),
                "pasos": state.pasos,
                "time_sec": round(float(t1 - t0), 4),
                "schedule_k": float(k),
                "schedule_lambda": float(lam),
                "schedule_limit": int(limit),
                "seed": self.global_seed
            })
        return times_problem, vals_problem

    # ---------- Batch runner ----------

    def _create_problem(self,initial_state, algoritmo, params):
        if initial_state == "empty":
            state = generate_initial_state_empty(params=params)
        elif initial_state == "random":
            state = generate_initial_state_random(params=params)
        elif initial_state == "greedy":
            state = generate_initial_state_greedy(params=params)
        else:
            raise ValueError("Initial state label not correct.")
        
        return GasProblem(initial_state=state, set_operadores=self.operators, algoritmo=algoritmo)

    def experimento(self, multiplicador:int = 0, initial_states: Optional[Tuple] = None, params: ProblemParameters = None, algoritmo: int = 0, schedule_params: Optional[Tuple[float, float, int]] = None, **versiones):
        """
        initial_state: ej -> ('empty', 'greedy')
        algoritmo: 0 -> hill climbing (HC), 1 -> simulated annealing (SA)
        versiones: pass as named arguments: nombre_variant=problem_instance
        Returns: self.cache: idx -> (name, (times_list, values_list))
        """
        # Clear in case of reuse
        self.cache.clear()
        if initial_states is None:
            names = list(versiones.keys())
            problems = list(versiones.values())
            for i, problem in enumerate(problems):
                label = names[i]
                print(f"--- Running variant: {label} ---")
                if algoritmo == 0:
                    times, values = self.experimento_hc(problem, label, multiplicador=multiplicador, reps=self.n)
                elif algoritmo == 1:
                    times, values = self.experimento_sa(problem, label, multiplicador=multiplicador, schedule_params=schedule_params, reps=self.n)
                else:
                    raise ValueError("algoritmo must be 0 (HC) or 1 (SA)")
                self.cache[i] = (label, (times, values))
        else:
            i = 0
            label = initial_states[1]
            for initial_state in initial_states[0]:
                print(f"--- Running variant: {label} ---")
                for j in range(self.n):
                    print(f"Repeticion {j}")
                    problem = self._create_problem(initial_state=initial_state, algoritmo=algoritmo, params = params)
                    
                    if algoritmo == 0:
                        times, values = self.experimento_hc(problem, label, multiplicador=multiplicador,  initial_state=initial_state, reps=1)
                    elif algoritmo == 1:
                        times, values = self.experimento_sa(problem, label, multiplicador=multiplicador, schedule_params=schedule_params, initial_state=initial_state, reps=1)
                    else:
                        raise ValueError("algoritmo must be 0 (HC) or 1 (SA)")
                
                i += 1

        return self.cache

    
    def to_table(self) -> List[dict]:
        """
        Returns a long-form list of rows. Each row has:
        variant, algorithm, run, beneficio, distancia, time_sec, schedule_k, schedule_lambda, schedule_limit, seed
        """
        return list(self.rows)

    def save_csv(self, filename: str = "resultados.csv") -> str:
        """
        Saves a CSV to out_dir. Returns full path.
        """
        import csv
        path = os.path.join(self.out_dir, filename)
        fieldnames = ["variant", "algorithm", "initial_state", "run", "multiplicador","beneficio", "distancia", "pasos", "peticiones_satisfechas","time_sec",
                    "schedule_k", "schedule_lambda", "schedule_limit", "seed"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)
        return path

    def save_json_summary(self, filename: str = "resumen.json") -> str:
        """
        Saves a per-variant, per-algorithm summary (mean, std, min, max) for beneficio, distancia, time.
        """
        summary = self.compute_summary()
        path = os.path.join(self.out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        return path

    def compute_summary(self) -> Dict[str, Dict[str, dict]]:
        """
        Returns nested dict: summary[variant][algorithm] -> metrics
        metrics include:
        n, beneficio_{mean, std, min, max, median}, distancia_{...}, time_sec_{...}
        """
        out: Dict[str, Dict[str, dict]] = {}
        # Build by variant and algorithm
        by_key: Dict[Tuple[str, str], List[dict]] = {}
        for r in self.rows:
            key = (r["variant"], r["algorithm"])
            by_key.setdefault(key, []).append(r)
        for (variant, algo), rows in by_key.items():
            ben = np.array([r["beneficio"] for r in rows], dtype=float)
            dis = np.array([r["distancia"] for r in rows], dtype=float)
            tms = np.array([r["time_sec"] for r in rows], dtype=float)
            pasos = np.array([r["pasos"] for r in rows], dtype=float)
            stats = {
                "n": len(rows),
                "beneficio_mean": float(ben.mean()),
                "beneficio_std": float(ben.std(ddof=1)) if len(ben) > 1 else 0.0,
                "beneficio_min": float(ben.min()),
                "beneficio_max": float(ben.max()),
                "beneficio_median": float(np.median(ben)),
                "distancia_mean": float(dis.mean()),
                "distancia_std": float(dis.std(ddof=1)) if len(dis) > 1 else 0.0,
                "distancia_min": float(dis.min()),
                "distancia_max": float(dis.max()),
                "distancia_median": float(np.median(dis)),
                "time_sec_mean": float(tms.mean()),
                "time_sec_std": float(tms.std(ddof=1)) if len(tms) > 1 else 0.0,
                "time_sec_min": float(tms.min()),
                "time_sec_max": float(tms.max()),
                "time_sec_median": float(np.median(tms)),
                "pasos_mean": round(pasos.mean())
            }
            out.setdefault(variant, {})[algo] = stats
        return out
    

    def _extract_by_variant(self) -> Dict[str, dict]:
        """
        Helper to group rows by (variant, algorithm) and return metric arrays.
        """
        by = {}
        for r in self.rows:
            key = (r["variant"], r["algorithm"])
            d = by.setdefault(key, {"beneficio": [], "distancia": [], "time_sec": []})
            d["beneficio"].append(r["beneficio"])
            d["distancia"].append(r["distancia"])
            d["time_sec"].append(r["time_sec"])
            d["pasos"].append(r["pasos"])
        return by

    def plot_box(self, metric: str = "beneficio", title: Optional[str] = None, filename: Optional[str] = None):
        """
        Boxplot per variant (and algorithm). Metric in {'beneficio','distancia','time_sec'}.
        Labels are shown as 'variant | algo'.
        """
        assert metric in {"beneficio", "distancia", "time_sec"}
        by = self._extract_by_variant()
        labels, data = [], []
        for (variant, algo), series in sorted(by.items()):
            labels.append(f"{variant} | {algo}")
            data.append(series[metric])

        plt.figure(figsize=(10, 5))
        plt.boxplot(data, labels=labels, showmeans=True)
        plt.xticks(rotation=30, ha="right")
        ylab = {
            "beneficio": "Beneficio",
            "distancia": "Distancia",
            "time_sec": "Tiempo (s)"
        }[metric]
        plt.ylabel(ylab)
        plt.title(title or f"Distribución de {ylab} por variante y algoritmo")
        plt.tight_layout()
        out = os.path.join(self.out_dir, filename or f"box_{metric}.png")
        plt.savefig(out, dpi=150)
        plt.close()
        return out

    def plot_beneficio_distancia_scatter(self, filename: str = "scatter_beneficio_distancia.png", show_pareto: bool = True):
        """
        Scatter plot of (distancia, beneficio) colored per variant|algo.
        Optionally overlays an estimated Pareto front (max beneficio, min distancia).
        """
        by = self._extract_by_variant()
        plt.figure(figsize=(8, 6))
        colors = plt.cm.get_cmap("tab20")
        keys_sorted = sorted(by.keys())
        for idx, key in enumerate(keys_sorted):
            (variant, algo) = key
            series = by[key]
            x = np.array(series["distancia"])
            y = np.array(series["beneficio"])
            plt.scatter(x, y, s=35, alpha=0.7, color=colors(idx % 20), label=f"{variant} | {algo}")

        if show_pareto:
            # Compute all points across all variants, then Pareto front (min distancia, max beneficio)
            xs, ys = [], []
            for series in by.values():
                xs.extend(series["distancia"])
                ys.extend(series["beneficio"])
            xs = np.array(xs)
            ys = np.array(ys)
            pareto_idx = self._pareto_front_indices(xs, ys)
            plt.plot(xs[pareto_idx], ys[pareto_idx], "k--", lw=2, label="Frontera Pareto (aprox)")

        plt.xlabel("Distancia")
        plt.ylabel("Beneficio")
        plt.title("Beneficio vs Distancia")
        plt.legend(loc="best", fontsize=8)
        plt.tight_layout()
        out = os.path.join(self.out_dir, filename)
        plt.savefig(out, dpi=150)
        plt.close()
        return out

    @staticmethod
    def _pareto_front_indices(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Approximate Pareto front assuming objectives: minimize x (distancia), maximize y (beneficio).
        Returns indices sorted by increasing x among non-dominated points.
        """
        # Sort by x asc, then sweep keeping strictly increasing best y
        order = np.argsort(x)
        x_sorted, y_sorted = x[order], y[order]
        best_y = -np.inf
        keep = []
        for i in range(len(x_sorted)):
            if y_sorted[i] > best_y:
                best_y = y_sorted[i]
                keep.append(i)
        return order[np.array(keep, dtype=int)]