from collections import defaultdict


class JobMatchEngine:

    SKILL_WEIGHT = 0.60
    DOMAIN_WEIGHT = 0.15
    INDUSTRY_WEIGHT = 0.15
    ROLE_WEIGHT = 0.10

    # =========================
    # 1️ SOFTWARE SKILL MATCH
    # =========================
    @staticmethod
    def skill_match(candidate, job):
        candidate_skills = set(
            candidate.software_skills.values_list('name', flat=True)
        )
        job_skills = set(
            job.required_skills.values_list('name', flat=True)
        )

        if not job_skills:
            return 0

        matched = candidate_skills & job_skills
        return round((len(matched) / len(job_skills)) * 100)

    # =========================
    # 2️ DOMAIN MATCH
    # =========================
    @staticmethod
    def domain_match(candidate, job):
        if not candidate.preferred_domains:
            return 0

        return 100 if job.domain in candidate.preferred_domains else 0

    # =========================
    # 3️ INDUSTRY MATCH
    # =========================
    @staticmethod
    def industry_match(candidate, job):
        if not candidate.preferred_industries:
            return 0

        return 100 if job.industry in candidate.preferred_industries else 0

    # =========================
    # 4️ JOB ROLE MATCH
    # =========================
    @staticmethod
    def role_match(candidate, job):
        if not candidate.preferred_job_roles:
            return 0

        return 100 if candidate.preferred_job_roles == job.job_role else 0

    # =========================
    #  FINAL SCORE
    # =========================
    @classmethod
    def final_match_percentage(cls, candidate, job):

        skill_score = cls.skill_match(candidate, job)
        domain_score = cls.domain_match(candidate, job)
        industry_score = cls.industry_match(candidate, job)
        role_score = cls.role_match(candidate, job)

        final_score = (
            skill_score * cls.SKILL_WEIGHT +
            domain_score * cls.DOMAIN_WEIGHT +
            industry_score * cls.INDUSTRY_WEIGHT +
            role_score * cls.ROLE_WEIGHT
        )

        return {
            "final_score": round(final_score),
            "skill_score": skill_score,
            "domain_score": domain_score,
            "industry_score": industry_score,
            "role_score": role_score
        }
