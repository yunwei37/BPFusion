import json,time
def external_request(client,ids,expected,key,observed):
    body=json.dumps({"token_ids":ids,"return_token_ids":True,"stream":True,
      "sampling_params":{"max_tokens":len(expected),"temperature":0.0,
                         "ignore_eos":True,"detokenize":False}},separators=(",",":")).encode()
    headers={"Content-Type":"application/json","Authorization":"Bearer "+key}
    start=time.monotonic_ns();observed.update(start_ns=start)
    client.request("POST","/inference/v1/generate",body,headers)
    response=client.getresponse()
    assert response.status==200,(response.status,response.read().decode())
    assert "text/event-stream" in response.getheader("Content-Type","")
    pending=b"";actual=[];arrivals=[];frames=[];done=False;prompt=None;finish=None
    observed.update(tokens=actual,arrival_ns=arrivals,frames=frames)
    while not done:
        data=response.read1(4096); arrived=time.monotonic_ns()
        assert data,"stream ended without DONE"
        pending+=data;observed["received_bytes"]=observed.get("received_bytes",0)+len(data)
        while b"\n\n" in pending:
            frame,pending=pending.split(b"\n\n",1)
            payload=b"\n".join(line[6:] for line in frame.splitlines() if line.startswith(b"data: "))
            if not payload: continue
            if payload==b"[DONE]": done=True;continue
            obj=json.loads(payload)
            if "prompt_token_ids" in obj: prompt=obj["prompt_token_ids"]
            for choice in obj["choices"]:
                assert choice["index"]==0,choice
                tokens=choice.get("token_ids") or []
                assert all(type(t)==int and 0<=t<151936 for t in tokens),tokens
                actual.extend(tokens);arrivals.extend([arrived]*len(tokens))
                if choice.get("finish_reason") is not None: finish=choice["finish_reason"]
            frames.append({"arrival_ns":arrived,"response":obj})
    tail=response.read(); assert not pending.strip() and not tail.strip(),(pending,tail)
    assert prompt==ids,(prompt,ids)
    assert len(actual)==len(expected),(actual,expected)
    assert finish=="length",finish
    return {"start_ns":start,"arrival_ns":arrivals,"tokens":actual,"exact_reference":actual==expected,
      "first_mismatch":next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None),
      "ttft_ms":(arrivals[0]-start)/1e6,"latency_ms":(arrivals[-1]-start)/1e6,
      "tpot_ms":(arrivals[-1]-arrivals[0])/(len(expected)-1)/1e6 if len(expected)>1 else None,
      "frames":frames}
