from dataclasses import dataclass

@dataclass
class Prompt:
    question: str
    answer: bool = None

def print_tier_description(tier=None):
    tier_descriptions = {
        0: "💡 Tier 0 - Private / Prototype: Private, experimental project, usually a single developer. No DPG indicators required yet.",
        1: "💡 Tier 1 - Public Release: Legally open and attributable. Mandatory indicators: approved open license (2), clear ownership (3), basic documentation (5).",
        2: "💡 Tier 2 - Maintained & Mission-Aligned: Sustained, purposeful. Adds SDG relevance (1), full documentation (5), and entry-level standards/best-practices (8).",
        3: "💡 Tier 3 - Open & Safe: Working in public with do-no-harm. Adds platform independence (4), non-PII data export (6), privacy & applicable laws (7), data privacy & security (9A).",
        4: "💡 Tier 4 - DPG-Ready / Eligible: Meets the full DPG Standard. Adds full standards (8) plus content moderation (9B) and harassment protection (9C) — all 9 indicators met → eligible to nominate to the DPG Registry."
    }

    if tier is None:
        for description in tier_descriptions.values():
            print(description)
    elif tier in tier_descriptions:
        print(tier_descriptions[tier])
    else:
        print(f"Invalid tier number: {tier}")

def main():
    # Intro text to repo-scaffolder
    print("\n👋 Welcome to the repo-scaffolder CLI.")
    print("⚙️  We will assist you with creating a repository.\n")

    print("🌱 This DPG-readiness maturity model classifies projects on their journey toward becoming a Digital Public Good:")
    print_tier_description()
    print("ℹ️  Visit https://github.com/UNDP/repo-scaffolder/blob/main/maturity-model-tiers.md for more information.")
    print("ℹ️  For an automated, evidence-based assessment of an existing repo (scoring all 9 DPG indicators), use the 'dpg-assess' Claude skill instead.\n")

    print("\n📝 Answer the following questions for a quick tier estimate of your project.")

    print("****************************************\n")

    prompts = {
        "CONTRIBUTORS": Prompt("Does your project have more than one contributor?"),
        "RELEASE": Prompt("Do you plan on shipping more than one release / maintaining it over time?"),
        "WORK": Prompt("Do you plan on having people outside your organization work with you?"),
        "MAINTAIN": Prompt("Do you plan on having people outside your organization maintain the project with you?"),
        "ROADMAP": Prompt("Do you plan on having people outside your organization help plan the development roadmap?")
    }

    # Obtain answers
    for key, prompt in prompts.items():
        while True:
            response = input(f"{prompt.question} [y/n]: ").strip().lower()
            if response in ["y", "yes"]:
                prompt.answer = True
                break
            elif response in ["n", "no"]:
                prompt.answer = False
                break
            else:
                print("Please answer y or n.")

    # Determine tier
    if not prompts["CONTRIBUTORS"].answer:
        tier = 0
    elif not prompts["RELEASE"].answer:
        tier = 0
    elif not prompts["WORK"].answer:
        tier = 1
    elif not prompts["MAINTAIN"].answer:
        tier = 2
    elif not prompts["ROADMAP"].answer:
        tier = 3
    else:
        tier = 4

    # Output results
    print(f"\n****************************************")
    print(f"\n📚 Your project is classified as: Tier {tier}")
    print_tier_description(tier)
    print(f"ℹ️  Visit https://github.com/UNDP/repo-scaffolder/blob/main/tier{tier} for more information about the maturity model tier.")

    # Provide next steps
    print(f"⚙️  Next, create your Tier {tier} repository by running the command below:")
    print(f"   cookiecutter https://github.com/UNDP/repo-scaffolder --directory=tier{tier}\n")
    

if __name__ == "__main__":
    main()