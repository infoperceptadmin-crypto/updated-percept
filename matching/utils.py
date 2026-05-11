class JobMatchEngine:

    SKILL_WEIGHT = 0.60
    DOMAIN_WEIGHT = 0.40

    @classmethod
    def calculate_match(cls, candidate_profile, job):
        # -------------------------
        # 1. SKILL MATCH (60%)
        # -------------------------
        job_skills_qs = job.skills_required.all()
        candidate_skills_qs = candidate_profile.software_skills.all()

        job_skills_lower = {s.skill_name.lower() for s in job_skills_qs}
        candidate_skills_lower = {s.skill_name.lower() for s in candidate_skills_qs}

        job_skills_original = [s.skill_name for s in job_skills_qs]

        matched_skills = []
        missing_skills = []

        if not job_skills_original:
            skill_score = 100
        else:
            for skill in job_skills_original:
                if skill.lower() in candidate_skills_lower:
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)

            skill_score = (len(matched_skills) / len(job_skills_original)) * 100

        # -------------------------
        # 2. DOMAIN MATCH (40%)
        # -------------------------
        job_domains = job.domains.all()
        domain_score = 0

        if job_domains.exists():
            candidate_domains = candidate_profile.preferred_domains.all()

            overlap = set(job_domains).intersection(set(candidate_domains))

            if overlap:
                domain_score = 100
        else:
            domain_score = 100

        # -------------------------
        # 3. FINAL CALCULATION
        # -------------------------
        final_score = (skill_score * cls.SKILL_WEIGHT) + (domain_score * cls.DOMAIN_WEIGHT)

        return int(final_score), matched_skills, missing_skills


def calculate_match_percentage(candidate_profile, job):
    return JobMatchEngine.calculate_match(candidate_profile, job)
