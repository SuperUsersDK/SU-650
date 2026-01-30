# import os

# import re

# import json

# import time

# import pickle

# from dataclasses import dataclass

# from pathlib import Path

# from typing import List, Tuple, Dict, Optional

# 

# import numpy as np

# from dotenv import load\_dotenv

# from openai import OpenAI

# 

# \# -----------------------------

# \# Konfiguration

# \# -----------------------------

# RAG\_DIR = Path("rag")

# INDEX\_PATH = Path("rag\_index.pkl")

# 

# EMBEDDING\_MODEL = "text-embedding-3-small"

# CHAT\_MODEL = "gpt-5"

# 

# \# Hvor mange top-chunks vi giver modellen

# TOP\_K = 6

# 

# \# "Hard gate": hvis bedste match er under denne, svar "det ved jeg ikke"

# \# Tip: 0.20-0.35 er ofte et fornuftigt start-interval afhængigt af data/chunking.

# SIMILARITY\_THRESHOLD = 0.28

# 

# \# Chunking

# CHUNK\_SIZE\_CHARS = 1200

# CHUNK\_OVERLAP\_CHARS = 200

# 

# 

# \# -----------------------------

# \# Datastrukturer

# \# -----------------------------

# @dataclass

# class Chunk:

# &nbsp;   doc\_id: str

# &nbsp;   source\_path: str

# &nbsp;   chunk\_id: int

# &nbsp;   text: str

# 

# @dataclass

# class IndexData:

# &nbsp;   chunks: List\[Chunk]

# &nbsp;   embeddings: np.ndarray  # shape (n, d), float32 normalized

# 

# 

# \# -----------------------------

# \# Hjælpefunktioner

# \# -----------------------------

# def iter\_text\_files(folder: Path) -> List\[Path]:

# &nbsp;   if not folder.exists():

# &nbsp;       raise FileNotFoundError(f"Mappen findes ikke: {folder.resolve()}")

# &nbsp;   files = \[]

# &nbsp;   for ext in ("\*.txt", "\*.md"):

# &nbsp;       files.extend(folder.rglob(ext))

# &nbsp;   return sorted(files)

# 

# def read\_text\_file(path: Path) -> str:

# &nbsp;   # Robust læsning: prøv utf-8 først, fallback latin-1

# &nbsp;   try:

# &nbsp;       return path.read\_text(encoding="utf-8")

# &nbsp;   except UnicodeDecodeError:

# &nbsp;       return path.read\_text(encoding="latin-1")

# 

# def normalize\_whitespace(s: str) -> str:

# &nbsp;   s = s.replace("\\u00a0", " ")

# &nbsp;   s = re.sub(r"\[ \\t]+", " ", s)

# &nbsp;   s = re.sub(r"\\n{3,}", "\\n\\n", s)

# &nbsp;   return s.strip()

# 

# def chunk\_text(text: str, size: int, overlap: int) -> List\[str]:

# &nbsp;   text = normalize\_whitespace(text)

# &nbsp;   if not text:

# &nbsp;       return \[]

# 

# &nbsp;   chunks = \[]

# &nbsp;   start = 0

# &nbsp;   n = len(text)

# &nbsp;   while start < n:

# &nbsp;       end = min(start + size, n)

# &nbsp;       chunk = text\[start:end].strip()

# &nbsp;       if chunk:

# &nbsp;           chunks.append(chunk)

# &nbsp;       if end == n:

# &nbsp;           break

# &nbsp;       start = max(0, end - overlap)

# &nbsp;   return chunks

# 

# def l2\_normalize(v: np.ndarray, eps: float = 1e-12) -> np.ndarray:

# &nbsp;   norm = np.linalg.norm(v, axis=-1, keepdims=True)

# &nbsp;   return v / np.maximum(norm, eps)

# 

# def cosine\_sim\_matrix(query\_vec: np.ndarray, mat: np.ndarray) -> np.ndarray:

# &nbsp;   # Forudsætter allerede L2-normaliserede vektorer

# &nbsp;   return mat @ query\_vec

# 

# def safe\_print\_sources(chunks\_with\_scores: List\[Tuple\[Chunk, float]]) -> None:

# &nbsp;   print("\\n\[Kilder brugt]")

# &nbsp;   for c, s in chunks\_with\_scores:

# &nbsp;       print(f"- {c.source\_path} (chunk {c.chunk\_id}, score {s:.3f})")

# 

# 

# \# -----------------------------

# \# OpenAI-klient

# \# -----------------------------

# def make\_client() -> OpenAI:

# &nbsp;   load\_dotenv()

# &nbsp;   if not os.getenv("OPENAI\_API\_KEY"):

# &nbsp;       raise RuntimeError("OPENAI\_API\_KEY mangler. Sæt den i miljøvariabel eller .env")

# &nbsp;   return OpenAI()

# 

# def embed\_texts(client: OpenAI, texts: List\[str]) -> np.ndarray:

# &nbsp;   # Batch embeddings (OpenAI håndterer batching server-side; vi kan sende en liste)

# &nbsp;   res = client.embeddings.create(

# &nbsp;       model=EMBEDDING\_MODEL,

# &nbsp;       input=texts,

# &nbsp;   )

# &nbsp;   vectors = np.array(\[d.embedding for d in res.data], dtype=np.float32)

# &nbsp;   vectors = l2\_normalize(vectors)

# &nbsp;   return vectors

# 

# 

# \# -----------------------------

# \# Indeksering

# \# -----------------------------

# def build\_or\_load\_index(client: OpenAI, force\_rebuild: bool = False) -> IndexData:

# &nbsp;   if INDEX\_PATH.exists() and not force\_rebuild:

# &nbsp;       with INDEX\_PATH.open("rb") as f:

# &nbsp;           obj = pickle.load(f)

# &nbsp;       # Basic sanity

# &nbsp;       if not isinstance(obj, IndexData):

# &nbsp;           raise RuntimeError("Index-fil har forkert format. Slet rag\_index.pkl og byg igen.")

# &nbsp;       return obj

# 

# &nbsp;   files = iter\_text\_files(RAG\_DIR)

# &nbsp;   if not files:

# &nbsp;       raise RuntimeError(f"Ingen .txt/.md filer fundet i {RAG\_DIR.resolve()}")

# 

# &nbsp;   chunks: List\[Chunk] = \[]

# &nbsp;   for fp in files:

# &nbsp;       doc\_text = read\_text\_file(fp)

# &nbsp;       parts = chunk\_text(doc\_text, CHUNK\_SIZE\_CHARS, CHUNK\_OVERLAP\_CHARS)

# &nbsp;       doc\_id = str(fp.relative\_to(RAG\_DIR))

# &nbsp;       for i, part in enumerate(parts):

# &nbsp;           chunks.append(Chunk(

# &nbsp;               doc\_id=doc\_id,

# &nbsp;               source\_path=str(fp),

# &nbsp;               chunk\_id=i,

# &nbsp;               text=part

# &nbsp;           ))

# 

# &nbsp;   # Embed alle chunks

# &nbsp;   # Hvis du har ekstremt mange chunks, kan du batch'e manuelt her.

# &nbsp;   texts = \[c.text for c in chunks]

# &nbsp;   embeddings = embed\_texts(client, texts)

# 

# &nbsp;   index = IndexData(chunks=chunks, embeddings=embeddings)

# 

# &nbsp;   with INDEX\_PATH.open("wb") as f:

# &nbsp;       pickle.dump(index, f)

# 

# &nbsp;   return index

# 

# 

# \# -----------------------------

# \# Retrieval + svarlogik (HARD GATE)

# \# -----------------------------

# def retrieve(index: IndexData, query\_vec: np.ndarray, top\_k: int) -> List\[Tuple\[Chunk, float]]:

# &nbsp;   sims = cosine\_sim\_matrix(query\_vec, index.embeddings)  # (n,)

# &nbsp;   top\_idx = np.argsort(-sims)\[:top\_k]

# &nbsp;   return \[(index.chunks\[i], float(sims\[i])) for i in top\_idx]

# 

# def should\_answer(chunks\_with\_scores: List\[Tuple\[Chunk, float]]) -> bool:

# &nbsp;   if not chunks\_with\_scores:

# &nbsp;       return False

# &nbsp;   best\_score = chunks\_with\_scores\[0]\[1]

# &nbsp;   return best\_score >= SIMILARITY\_THRESHOLD

# 

# def build\_context(chunks\_with\_scores: List\[Tuple\[Chunk, float]]) -> str:

# &nbsp;   # Kort og tydelig kontekst med kildeinfo

# &nbsp;   blocks = \[]

# &nbsp;   for c, s in chunks\_with\_scores:

# &nbsp;       blocks.append(

# &nbsp;           f"\[KILDE: {c.doc\_id} | chunk {c.chunk\_id} | score {s:.3f}]\\n{c.text}"

# &nbsp;       )

# &nbsp;   return "\\n\\n---\\n\\n".join(blocks)

# 

# def answer\_with\_rag(client: OpenAI, index: IndexData, user\_question: str) -> Tuple\[str, Optional\[List\[Tuple\[Chunk, float]]]]:

# &nbsp;   q\_vec = embed\_texts(client, \[user\_question])\[0]

# &nbsp;   retrieved = retrieve(index, q\_vec, TOP\_K)

# 

# &nbsp;   # HARD GATE: hvis ikke tydeligt i docs => "det ved jeg ikke"

# &nbsp;   if not should\_answer(retrieved):

# &nbsp;       return "det ved jeg ikke", None

# 

# &nbsp;   context = build\_context(retrieved)

# 

# &nbsp;   instructions = (

# &nbsp;       "Du er en intern chatbot. Du må KUN svare ud fra den givne KONTEKST.\\n"

# &nbsp;       "Hvis svaret ikke står i KONTEKSTEN, skal du svare præcist: det ved jeg ikke\\n"

# &nbsp;       "Du må ikke gætte, antage, eller finde på.\\n"

# &nbsp;       "Svar kort og præcist på dansk."

# &nbsp;   )

# 

# &nbsp;   # Responses API (anbefalet i docs)

# &nbsp;   resp = client.responses.create(

# &nbsp;       model=CHAT\_MODEL,

# &nbsp;       instructions=instructions,

# &nbsp;       input=\[

# &nbsp;           {"role": "user", "content": f"KONTEKST:\\n{context}\\n\\nSPØRGSMÅL:\\n{user\_question}"}

# &nbsp;       ],

# &nbsp;   )

# 

# &nbsp;   # Udpak tekst-output

# &nbsp;   # (Responses API kan returnere flere output items; vi samler tekst)

# &nbsp;   parts = \[]

# &nbsp;   for item in resp.output:

# &nbsp;       if item.type == "message":

# &nbsp;           for c in item.content:

# &nbsp;               if c.type == "output\_text":

# &nbsp;                   parts.append(c.text)

# &nbsp;   text = "\\n".join(parts).strip()

# 

# &nbsp;   # Ekstra sikkerhed: hvis modellen ikke følger reglen, så håndhæv.

# &nbsp;   if not text:

# &nbsp;       return "det ved jeg ikke", None

# 

# &nbsp;   # Hvis den skriver noget andet end "det ved jeg ikke" men uden kildegrundlag,

# &nbsp;   # er det svært at verificere perfekt; hard gate tager det meste.

# &nbsp;   # Vi håndhæver dog stadig exact fallback hvis den selv siger den ikke ved.

# &nbsp;   lowered = text.strip().lower()

# &nbsp;   if "det ved jeg ikke" in lowered and lowered != "det ved jeg ikke":

# &nbsp;       # hvis den fx skriver "Det ved jeg ikke, men..." -> stop den.

# &nbsp;       return "det ved jeg ikke", None

# 

# &nbsp;   return text, retrieved

# 

# 

# \# -----------------------------

# \# CLI Chat loop

# \# -----------------------------

# def main():

# &nbsp;   client = make\_client()

# 

# &nbsp;   print("Indlæser / bygger indeks fra rag/ ...")

# &nbsp;   index = build\_or\_load\_index(client, force\_rebuild=False)

# &nbsp;   print(f"Klar. Indlæst {len(index.chunks)} chunks fra {RAG\_DIR}/")

# &nbsp;   print("Skriv 'reindex' for at genbygge indeks, eller 'exit' for at afslutte.\\n")

# 

# &nbsp;   while True:

# &nbsp;       user\_q = input("Du: ").strip()

# &nbsp;       if not user\_q:

# &nbsp;           continue

# &nbsp;       if user\_q.lower() in ("exit", "quit"):

# &nbsp;           break

# &nbsp;       if user\_q.lower() == "reindex":

# &nbsp;           print("Genbygger indeks ...")

# &nbsp;           index = build\_or\_load\_index(client, force\_rebuild=True)

# &nbsp;           print(f"Færdig. {len(index.chunks)} chunks.\\n")

# &nbsp;           continue

# 

# &nbsp;       answer, sources = answer\_with\_rag(client, index, user\_q)

# &nbsp;       print(f"\\nBot: {answer}\\n")

# 

# &nbsp;       # Valgfrit: vis hvilke kilder der blev brugt (godt internt)

# &nbsp;       if sources is not None:

# &nbsp;           safe\_print\_sources(sources)

# &nbsp;           print()

# 

# if \_\_name\_\_ == "\_\_main\_\_":

# &nbsp;   main()

# 

