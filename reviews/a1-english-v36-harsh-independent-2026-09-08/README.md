# A1 v36 — independent referee review

**Reviewed manuscript:** `8f074b8027627a71a81a362b9d15f47975e1f3ae`.  
**Review branch:** `review/a1-english-v36-harsh-independent-2026-09-08`.  
**Recommendation:** Accept the main article; no further mandatory mathematical revision requested.

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the complete assessment, precise mathematical scope and source ledger. This is an owner-requested AI-assisted referee-style recommendation, not an actual journal commission or acceptance.

## 本轮结论

R35.1 和 R35.2 均已关闭。共同归一化 H = 16 和固定 L >= 8 使三个采集长度问题在同一校准下具有完全相同的辅助 Fourier 矩阵；平坦路径的交叉预算明确只是风险比较包络的量级，不是最优控制器改变结构的精确整数阈值。

本轮没有发现足以推翻已审计主定理链的反例或致命证明缺口。正面建议依据是实际采集切空间、合流方向的概率质量、完整像的覆盖，以及逐报告计费的共同因果实现，而不是编译成功或测试数量。意见不扩展为对全部 companion 或十一篇论文的认证。

## Independently executed production

Both complete native volumes were rebuilt from the verified 80-input closure: 42 main pages and 159 companion pages, six successful compiler invocations, stable actual external labels and no final unresolved references or overfull boxes. Every page's extracted text matches the supplied PDFs; 13 sampled raster comparisons match exactly. PDF byte identity is not claimed.

Five existing mathematical programs were replayed normally and with `-O`; all ten outputs match their published hashes. The additional independent source-delta checker verifies 222 preserved statement blocks and 210 proof blocks, with exactly the two stated statement changes and one augmented proof. Diagnostics are not continuum proof verification or global controller optimization.

## Reproduce

Obtain the pinned v36 native source package and the preceding v35 native/review packages. Use separate working and output directories. Python 3.10+, a complete TeX installation, SymPy, mpmath, PyMuPDF and Pillow cover the tools used below.

```sh
python audit/reproduce_native.py --source-root /path/to/v36 --work-root /tmp/v36-referee-new
python audit/replay_diagnostics.py --source-root /tmp/v36-referee-new --previous-review /path/to/v35-review --output-root /tmp/v36-replays-new
python audit/check_revision_delta.py --old-root /path/to/v35 --new-root /path/to/v36
python audit/check_production.py --original-root /path/to/v36 --rebuilt-root /tmp/v36-referee-new --output-root /tmp/v36-production-new
```

`AUDIT_RECORD.json` records the execution, file identities and exact coverage limits. The full source-identity, native build, replay and production receipts and raw compiler stdout logs accompany the local review package. Source manifests under `audit/source-manifests/` are explicitly author records used to pin the input objects, not independent referee build receipts.

The mathematical source is not edited by any review script. New repository files are confined to this review directory. No GitHub Actions, formal proof assistant, exhaustive originality search or complete companion proof audit is claimed.
