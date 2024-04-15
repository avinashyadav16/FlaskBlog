# FlaskBlog

A full-fledged blog application build using flask.

#### To Generate the Secret Key in FlaskBlog.py File:

1. Open the terminal:
2. Run the below command:

   ```bash
   >>> python
   >>> import secrets
   >>> secrets.token_hex(16)
   ```

3. Copy the generated key and paste it in the FlaskBlog.py file in the place of "GENERATED_KEY"
   `app.config['SECRET_KEY'] = 'GENERATED_KEY'`

4. Save the file and run the application.
