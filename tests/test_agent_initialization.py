import importlib
import sys

import pytest


def _reload_module(module_name: str):
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


def test_pure_agent_module_import_does_not_require_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    module = _reload_module("agents.pure_agent")

    assert hasattr(module, "PureAgent")


def test_rag_agent_does_not_build_embeddings_without_vector_db(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    module = _reload_module("agents.rag_agent")

    class DummyModel:
        def generate_content(self, _prompt, **_kwargs):
            return type("Response", (), {"text": "ok"})()

    called = {"embeddings": 0}

    def fake_embeddings(*_args, **_kwargs):
        called["embeddings"] += 1
        return object()

    monkeypatch.setattr(module.genai, "configure", lambda **_kwargs: None)
    monkeypatch.setattr(module.genai, "GenerativeModel", lambda _name: DummyModel())
    monkeypatch.setattr(module, "HuggingFaceEmbeddings", fake_embeddings)
    monkeypatch.setattr(module, "DB_DIR", "Z:/definitely_missing_db")

    agent = module.RAGAgent()

    assert agent.vectorstore is None
    assert called["embeddings"] == 0


def test_pure_agent_requires_api_key_at_runtime(monkeypatch):
    module = _reload_module("agents.pure_agent")
    monkeypatch.setattr(module.os, "getenv", lambda _name: None)

    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        module.PureAgent()
