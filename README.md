# How a Forced Navier–Stokes Flow Blows Up

A guided exposition of OpenAI's finite-time blowup construction for the
three-dimensional incompressible Navier–Stokes equations.

**[Read the PDF](ns_exposition.pdf)** (15 pages) · LaTeX source: [`ns_exposition.tex`](ns_exposition.tex)

Author: Thanh Van Nguyen · Version 1.0 · 29 October 2026

## Scope

In September 2026 OpenAI released *Finite time blowup for Navier–Stokes*
([PDF](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf))
and a Lean 4 formalization
([openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler),
commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`). For every viscosity
ν > 0, the paper constructs a smooth, compactly supported force and a
velocity field that starts from rest, keeps bounded kinetic energy, and becomes
unbounded at t = 1. This addresses the forced breakdown alternatives (C) and (D)
of the Clay Millennium Problem. The unforced alternatives (A) and (B) remain open.

The exposition covers:

- the reformulation of the problem as a cancellation problem for the momentum residual;
- the anisotropic collapsing vortex and its scales;
- the annular stress, and how amplified oscillatory pulses supply it;
- the infinite-order correction cycle and its summation;
- localization, the force extension past t = 1, the energy bound, uniqueness, and the torus case;
- what the Lean development certifies;
- a reading map of the 166-page paper and a glossary.

Each statement is tagged by provenance:

| Tag | Meaning |
| --- | --- |
| **[Paper]** | Taken from the source paper, with its location given. |
| **[Check]** | A computation the author verified independently. |
| **[Heuristic]** | A simplified model that conveys a mechanism. |
| **[Context]** | Background from the wider literature. |

## Status of the underlying result

As of 29 October 2026, the result has not been independently peer reviewed.
The author of this exposition did not rebuild the Lean project. All
mathematical results are due to the authors of the cited works. This document
contributes exposition only.

This exposition concerns problem
[JSP-000005](https://github.com/TheJustinSunPrize/awards/blob/main/problems/catalog-0001-0100.md#JSP-000005)
of The Justin Sun Prize problem bank ([MathDB #315852](https://mathdb.com/p/315852/navier-stokes-existence-and-smoothness)).

## AI assistance

The exposition was prepared with the assistance of an AI system (Claude, Anthropic).
Every statement attributed to the source paper was checked against the pinned
PDF and repository.

## Building

```sh
latexmk -pdf ns_exposition.tex
```

## Citation

> Thanh Van Nguyen, *How a Forced Navier–Stokes Flow Blows Up: A guided exposition of
> OpenAI's finite-time blowup construction*, version 1.0, 29 October 2026.
> https://github.com/Thanh-Van-2001/navier-stokes-blowup-exposition

## License

Text and figures: [CC BY 4.0](LICENSE).
