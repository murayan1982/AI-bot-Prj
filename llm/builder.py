from llm.factory import create_llm, get_supported_llm_providers
from llm.fallback_llm import FallbackLLM
from llm.router_llm import RouterLLM
from registry.llm import LLM_CATALOG, LLM_ROUTES


def _resolve_llm_config(llm_name: str) -> dict:
    if llm_name not in LLM_CATALOG:
        raise ValueError(f"Unknown LLM catalog entry: {llm_name}")
    return LLM_CATALOG[llm_name]


def validate_llm_registry() -> None:
    supported_providers = get_supported_llm_providers()

    for llm_name, llm_config in LLM_CATALOG.items():
        provider = llm_config.get("provider")
        model = llm_config.get("model")

        if not provider:
            raise ValueError(f"LLM catalog entry '{llm_name}' has no provider.")

        if not model:
            raise ValueError(f"LLM catalog entry '{llm_name}' has no model.")

        if provider not in supported_providers:
            raise ValueError(
                f"LLM catalog entry '{llm_name}' uses unsupported provider: {provider}"
            )

    for route_name, route_config in LLM_ROUTES.items():
        primary_name = route_config.get("primary")
        fallback_name = route_config.get("fallback")

        if primary_name not in LLM_CATALOG:
            raise ValueError(
                f"LLM route '{route_name}' has unknown primary: {primary_name}"
            )

        if fallback_name not in LLM_CATALOG:
            raise ValueError(
                f"LLM route '{route_name}' has unknown fallback: {fallback_name}"
            )


def _build_single_llm(llm_name: str, system_instruction: str):
    llm_config = _resolve_llm_config(llm_name)

    return create_llm(
        provider=llm_config["provider"],
        model=llm_config["model"],
        system_instruction=system_instruction,
    )


def _build_fallback_llm(route_config: dict, system_instruction: str):
    primary_name = route_config["primary"]
    fallback_name = route_config["fallback"]

    primary = _build_single_llm(
        llm_name=primary_name,
        system_instruction=system_instruction,
    )

    fallback = _build_single_llm(
        llm_name=fallback_name,
        system_instruction=system_instruction,
    )

    return FallbackLLM(primary, fallback)


def build_llm(system_instruction: str):
    chat_llm = _build_fallback_llm(
        route_config=LLM_ROUTES["chat"],
        system_instruction=system_instruction,
    )

    code_llm = _build_fallback_llm(
        route_config=LLM_ROUTES["code"],
        system_instruction=system_instruction,
    )

    return RouterLLM(chat_llm, code_llm)