import pandas as pd
import re
from fuzzywuzzy import fuzz
import unidecode

class ConditionExtractor:
      def __init__(self, df_players, df_coaches, df_doctors):
          self.df_players = df_players
          self.df_coaches = df_coaches
          self.df_doctors = df_doctors

          self.position_keywords = {
              "goalkeeper": "GK", "defender": "CB", "midfielder": "CMF",
              "striker": "CF", "forward": "CF", "winger": "LWF", "attacker": "CF"
          }
          # 🔁 Inverse du mapping formation_to_style
          self.coach_formation_keywords = {
              "offensif": "4-3-3 attacking",
              "offensive": "4-3-3 attacking",
              "equilibre": "4-2-3-1",
              "balanced": "4-2-3-1",
              "defensif": "5-3-2",
              "defensive": "5-3-2"
          }

          self.formation_to_style = {
              '4-3-3 attacking': 'offensif',
              '3-4-2-1': 'offensif',
              '4-2-3-1': 'equilibre',
              '4-1-4-1': 'equilibre',
              '4-4-2 double 6': 'equilibre',
              '4-3-1-2': 'equilibre',
              '3-5-2 flat': 'equilibre',
              '4-4-2': 'equilibre',
              '5-3-2': 'defensif',
              '4-4-2 diamond': 'equilibre',
              '3-4-1-2': 'offensif',
              '4-4-1-1': 'defensif',
              '3-4-3': 'offensif',
              '3-5-2': 'equilibre',
              '4-3-3': 'offensif',
              '4-4-1-1': 'equilibre',
              '5-4-1': 'defensif'
          }


          # ✅ Initialiser le mapping style → formations
          self.style_to_formations = {}

          for formation, style in self.formation_to_style.items():
              style = style.lower()
              if style not in self.style_to_formations:
                  self.style_to_formations[style] = []
              self.style_to_formations[style].append(formation)

          self.coach_licence_keywords = {
              "uefa": "UEFA Pro",
              "beginner": "National C"
          }

          self.stopwords = {'un', 'une', 'le', 'la', 'et', 'avec', 'bonne', 'de', 'des', 'du',
                            'à', 'a', 'an', 'the', 'good', 'with', 'coach', 'looking', 'for', 'and', 'years'}
      def filter_players_by_conditions(self, df, conditions):
          """
          Applique les conditions (autres que 'registered_position') sur un DataFrame de joueurs recommandés.
          """
          for col, op, val in conditions:
              if col == 'registered_position':
                  continue  # déjà appliqué

              if col not in df.columns:
                  continue

              try:
                  if op == '==':
                      df = df[df[col] == val]
                  elif op == '>':
                      df = df[df[col] > val]
                  elif op == '<':
                      df = df[df[col] < val]
                  elif op == '>=':
                      df = df[df[col] >= val]
                  elif op == '<=':
                      df = df[df[col] <= val]
              except Exception as e:
                  print(f"⚠️ Erreur lors du filtrage sur {col} {op} {val} : {e}")

          return df

      def clean(self, text):
          return unidecode.unidecode(text.lower().strip())
      def extract_doctor_specialty(self, text):
              text_clean = self.clean(text)

              # Liste unique des spécialités dans le df docteurs
              if 'specialty' not in self.df_doctors.columns:
                  return []

              specialties = self.df_doctors['specialty'].dropna().unique()
              specialties_clean = [self.clean(s) for s in specialties]

              # Fuzzy match : trouver la spécialité la plus proche dans la phrase
              best_match, score = process.extractOne(text_clean, specialties_clean)

              # Seuil à ajuster (ex: 70%)
              if score >= 70:
                  # Retrouver la spécialité originale correspondant au match nettoyé
                  original_specialty = specialties[specialties_clean.index(best_match)]
                  print(f"✅ Spécialité détectée par fuzzy matching : {original_specialty} (score {score})")
                  return [("specialty", "==", original_specialty)]

              return []
      def extract_formation_from_style(self, text):
          """
          Détecte un style (offensive, defensive, équilibré) et retourne une formation correspondante.
          """
          text = self.clean(text)
          tokens = text.split()

          detected_style = None
          for word in tokens:
              if word in ['offensif']:
                  detected_style = 'offensif'
              elif word in ['balanced']:
                  detected_style = 'equilibre'
              elif word in ['defensif']:
                  detected_style = 'defensif'

          if detected_style and detected_style in self.style_to_formations:
              # Retourne la première formation correspondante à ce style
              return self.style_to_formations[detected_style][0]

          return None

      def detect_profile(self, text):
          text = self.clean(text)
          if "doctor" in text or "cardiologist" in text or "beneficiaries" in text:
              columns = [c for c in self.df_doctors.columns if c not in ['Rndrng_Prvdr_First_Name', 'Rndrng_Prvdr_Last_Org_Name']]
              return "doctor", self.df_doctors, columns
          elif fuzz.partial_ratio("player", text) >= fuzz.partial_ratio("coach", text):
              return "player", self.df_players, list(self.df_players.columns)
          else:
              return "coach", self.df_coaches, list(self.df_coaches.columns)

      def extract_categorical_conditions(self, text, df):
          found = []
          text = self.clean(text)
          for keyword, value in self.position_keywords.items():
              if keyword in text and 'registered_position' in df.columns:
                  found.append(('registered_position', '==', value))
          return found

      def extract_coach_conditions(self, text, df):
          found = []
          text = self.clean(text)

          # Formation via mots-clés connus
          for word in text.split():
              word_clean = self.clean(word)

              if word_clean in self.coach_formation_keywords and 'preffered_formation' in df.columns:
                  formation = self.coach_formation_keywords[word_clean]
                  found.append(("preffered_formation", "==", formation))

          # Licence via fuzzy matching seulement si le mot "licence" est proche
          if 'coaching_licence' in df.columns and "licence" in text:
              # Recherche simple par mot-clé
              for keyword, licence_val in self.coach_licence_keywords.items():
                  if keyword in text:
                      print(f"✅ Licence match keyword détecté: {licence_val} (mot-clé: {keyword})")
                      found.append(("coaching_licence", "==", licence_val))
                      break

              else:
                  # Fallback fuzzy matching complet
                  all_licences = df['coaching_licence'].dropna().unique().astype(str)
                  for val in all_licences:
                      val_clean = self.clean(val)
                      score = fuzz.token_set_ratio(val_clean, text)
                      if score >= 90:
                          print(f"✅ Licence match fuzzy trouvée: {val} avec score {score}")
                          found.append(("coaching_licence", "==", val))
                          break



          return found



      def extract_numeric_conditions(self, text, columns, df, debug=False):
          text = self.clean(text)
          condition_map = {
              "greater than": ">", "less than": "<", "equal to": "==",
              "more than": ">", "under": "<", "over": ">", "=": "==",
              "inferieur a": "<", "superieur a": ">", "egal a": "==",
              "<": "<", ">": ">", "<=": "<=", ">=": ">="
          }

          found = []
          for phrase, op in condition_map.items():
              pattern = rf"(\b[\w\s]{{1,40}}?)\s*{re.escape(phrase)}\s*([\d\.]+)"
              matches = re.findall(pattern, text, flags=re.IGNORECASE)
              for raw_phrase, value in matches:
                  phrase_clean = self.clean(" ".join(raw_phrase.split()[-3:]))
                  best_score = 0
                  best_col = None
                  for col in columns:
                      if pd.api.types.is_numeric_dtype(df[col]):
                          col_name_clean = self.clean(col.replace("_", " "))
                          score = fuzz.token_set_ratio(phrase_clean, col_name_clean)
                          if debug:
                              print(f"🧠 Numeric match: '{phrase_clean}' vs '{col_name_clean}' → {score}")
                          if score > best_score and score >= 50:
                              best_score = score
                              best_col = col
                  if best_col:
                      if debug:
                          print(f"✅ Matched numeric condition: {best_col} {op} {value}")
                      found.append((best_col, op, float(value)))
          return found

      def extract_text_conditions(self, text, df, columns, debug=False):
          found = []
          text_clean = self.clean(text)
          used_cols = set()
          tokens = set(self.clean(w) for w in re.findall(r'\b\w+\b', text))
          ngrams = [" ".join(list(tokens)[i:j]) for i in range(len(tokens)) for j in range(i+1, min(i+4, len(tokens)+1))]

          for col in columns:
              if col in used_cols or not pd.api.types.is_object_dtype(df[col]):
                  continue
              values = df[col].dropna().unique().astype(str)
              for val in values:
                  val_clean = self.clean(val)
                  val_tokens = set(val_clean.split())
                  if len(tokens.intersection(val_tokens)) >= 2:
                      for phrase in ngrams:
                          score = fuzz.token_set_ratio(val_clean, phrase)
                          if debug:
                              print(f"🧠 Text match: '{phrase}' vs '{val_clean}' → {score}")
                          if score >= 90 and phrase in text_clean:
                              if debug:
                                  print(f"✅ Matched text condition: {col} == {val}")
                              found.append((col, '==', val))
                              used_cols.add(col)
                              break
              if col in used_cols:
                  break
          return found

      def extract_all(self, text, debug=False):
          profile, df, columns = self.detect_profile(text)

          categorical = []
          if profile == 'player':
              categorical = self.extract_categorical_conditions(text, df)
          elif profile == 'coach':
              categorical = self.extract_coach_conditions(text, df)
          elif profile == 'doctor':
              categorical = self.extract_doctor_specialty(text)

          numeric = self.extract_numeric_conditions(text, columns, df, debug=debug)
          text_conditions = self.extract_text_conditions(text, df, columns, debug=debug) if profile == 'doctor' else []

          conditions = numeric + categorical + text_conditions
          extracted_columns = list({col for col, _, _ in conditions})

          return {
              "profile": profile,
              "columns": extracted_columns,
              "conditions": conditions
          }
