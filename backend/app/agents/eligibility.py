import json
from typing import Dict, Any, List, Tuple

class EligibilityAgent:
    def __init__(self):
        pass

    def evaluate_scheme(self, user_profile: Dict[str, Any], scheme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Matches a single scheme against the user profile.
        Returns:
            {
                "eligible": bool,
                "status": str ("Highly Eligible", "Eligible", "Potentially Eligible", "Ineligible"),
                "match_percentage": int,
                "reasons": List[str],
                "missing_profile_fields": List[str]
            }
        """
        rules = scheme.get("eligibility_rules", {})
        reasons = []
        ineligible_reasons = []
        missing_profile_fields = []
        
        # Track matching points
        total_checks = 0
        passed_checks = 0
        
        # Helper to check if a profile field is empty/None
        def is_empty(val):
            return val is None or val == ""

        # 1. State check
        scheme_state = scheme.get("state", "Central")
        user_state = user_profile.get("state")
        if scheme_state != "Central" and scheme_state:
            total_checks += 1
            if is_empty(user_state):
                missing_profile_fields.append("state")
            elif user_state.lower() != scheme_state.lower():
                ineligible_reasons.append(f"Scheme is restricted to residents of {scheme_state} (User lives in {user_state or 'Unknown'})")
            else:
                passed_checks += 1
                reasons.append(f"Residency matches state: {scheme_state}")

        # 2. Occupation check
        allowed_occupations = rules.get("occupations", [])
        user_occupation = user_profile.get("occupation")
        if allowed_occupations:
            total_checks += 1
            if is_empty(user_occupation):
                missing_profile_fields.append("occupation")
            elif user_occupation not in allowed_occupations:
                ineligible_reasons.append(f"Scheme is for {', '.join(allowed_occupations)} (User is {user_occupation or 'Not Specified'})")
            else:
                passed_checks += 1
                reasons.append(f"Occupation matches: {user_occupation}")

        # 3. Income check
        max_income = rules.get("max_income")
        user_income = user_profile.get("income")
        if max_income is not None:
            total_checks += 1
            if is_empty(user_income):
                missing_profile_fields.append("income")
            elif user_income > max_income:
                ineligible_reasons.append(f"Income is ₹{user_income:,.2f}, which exceeds the limit of ₹{max_income:,.2f}")
            else:
                passed_checks += 1
                reasons.append(f"Family income (₹{user_income:,.2f}) is below the threshold of ₹{max_income:,.2f}")

        # 4. Age Check
        min_age = rules.get("min_age", 0)
        max_age = rules.get("max_age", 120)
        user_age = user_profile.get("age")
        if user_age is not None:
            total_checks += 1
            if user_age < min_age or user_age > max_age:
                ineligible_reasons.append(f"Age {user_age} is outside the allowed range of {min_age} to {max_age} years")
            else:
                passed_checks += 1
                reasons.append(f"Age {user_age} is within the eligibility range ({min_age} - {max_age} years)")
        else:
            missing_profile_fields.append("age")

        # 5. Gender check
        allowed_genders = rules.get("genders", [])
        user_gender = user_profile.get("gender")
        if allowed_genders:
            total_checks += 1
            if is_empty(user_gender):
                missing_profile_fields.append("gender")
            elif user_gender not in allowed_genders:
                ineligible_reasons.append(f"Scheme is for {', '.join(allowed_genders)} (User is {user_gender or 'Not Specified'})")
            else:
                passed_checks += 1
                reasons.append(f"Gender matches: {user_gender}")

        # 6. Social category check
        allowed_categories = rules.get("social_categories", [])
        user_cat = user_profile.get("social_category")
        if allowed_categories:
            total_checks += 1
            if is_empty(user_cat):
                missing_profile_fields.append("social_category")
            elif user_cat not in allowed_categories:
                ineligible_reasons.append(f"Scheme is restricted to {', '.join(allowed_categories)} categories (User is {user_cat or 'Not Specified'})")
            else:
                passed_checks += 1
                reasons.append(f"Category matches: {user_cat}")

        # 7. Landholder check
        land_req = rules.get("landholder")
        user_land = user_profile.get("landholder")
        if land_req is not None:
            total_checks += 1
            if is_empty(user_land):
                missing_profile_fields.append("landholder")
            elif user_land != land_req:
                ineligible_reasons.append("Landholder status does not match requirements for this agricultural scheme")
            else:
                passed_checks += 1
                reasons.append("Landownership status matches criteria")

        # 8. Disability check
        disability_req = rules.get("is_disabled")
        user_dis = user_profile.get("is_disabled")
        if disability_req is not None:
            total_checks += 1
            if is_empty(user_dis):
                missing_profile_fields.append("is_disabled")
            elif user_dis != disability_req:
                ineligible_reasons.append("Disability status mismatch")
            else:
                passed_checks += 1
                reasons.append("Disability status matches criteria")

        # 9. Own House check (Requires lack of own house)
        house_req = rules.get("requires_own_house")
        user_house = user_profile.get("requires_own_house")
        if house_req is not None:
            total_checks += 1
            if is_empty(user_house):
                missing_profile_fields.append("requires_own_house")
            elif user_house != house_req:
                ineligible_reasons.append("Applicant owns a pucca house, which disqualifies them from this housing support scheme")
            else:
                passed_checks += 1
                reasons.append("Does not own a pucca house (matches housing scheme requirement)")

        # 10. Widow Check
        widow_req = rules.get("is_widow")
        user_widow = user_profile.get("is_widow")
        user_marital = user_profile.get("marital_status")
        if widow_req is not None:
            total_checks += 1
            is_user_widow = (user_marital == "Widow") if user_marital else None
            if is_empty(user_marital):
                missing_profile_fields.append("marital_status")
            elif is_user_widow != widow_req:
                ineligible_reasons.append("Marital/widow status mismatch")
            else:
                passed_checks += 1
                reasons.append("Widowed status matches pension requirements")

        # 11. Senior Citizen Check
        senior_req = rules.get("is_senior_citizen")
        user_senior = user_profile.get("is_senior_citizen")
        if senior_req is not None:
            total_checks += 1
            calculated_senior = (user_age >= 60) if user_age is not None else None
            if calculated_senior is None:
                missing_profile_fields.append("age")
            elif calculated_senior != senior_req:
                ineligible_reasons.append("Senior citizen status mismatch")
            else:
                passed_checks += 1
                reasons.append("Senior citizen age criteria met")

        # Calculate final eligibility status
        if ineligible_reasons:
            eligible = False
            status = "Ineligible"
            match_percentage = int((passed_checks / max(total_checks, 1)) * 100)
            reasons.extend(ineligible_reasons)
        else:
            eligible = True
            
            # Determine match percentage
            if total_checks > 0:
                match_percentage = int((passed_checks / total_checks) * 100)
            else:
                match_percentage = 100
                
            # If there are missing fields, mark as Potentially Eligible
            if missing_profile_fields:
                status = "Potentially Eligible"
            else:
                # Calculate document readiness
                req_docs = scheme.get("required_documents", [])
                user_docs = user_profile.get("available_documents", [])
                
                # Count available required docs
                available_req_docs = sum(1 for d in req_docs if d in user_docs)
                total_docs = len(req_docs)
                
                doc_readiness = (available_req_docs / max(total_docs, 1))
                if doc_readiness >= 0.75:
                    status = "Highly Eligible"
                else:
                    status = "Eligible"
                    
        return {
            "eligible": eligible,
            "status": status,
            "match_percentage": match_percentage,
            "reasons": reasons,
            "missing_profile_fields": missing_profile_fields
        }

    def evaluate_all_schemes(self, user_profile: Dict[str, Any], schemes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Filters and evaluates all schemes.
        """
        results = {
            "Highly Eligible": [],
            "Eligible": [],
            "Potentially Eligible": [],
            "Ineligible": []
        }
        
        for s in schemes:
            eval_res = self.evaluate_scheme(user_profile, s)
            
            scheme_res = {
                "scheme_id": s.get("scheme_id"),
                "scheme_name": s.get("scheme_name"),
                "ministry": s.get("ministry"),
                "state": s.get("state"),
                "benefits": s.get("benefits"),
                "required_documents": s.get("required_documents"),
                "application_steps": s.get("application_steps"),
                "official_link": s.get("official_link"),
                "faqs": s.get("faqs"),
                "match_percentage": eval_res["match_percentage"],
                "reasons": eval_res["reasons"],
                "status": eval_res["status"],
                "missing_profile_fields": eval_res["missing_profile_fields"]
            }
            
            results[eval_res["status"]].append(scheme_res)
            
        return results
