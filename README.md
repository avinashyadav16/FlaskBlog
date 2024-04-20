# FlaskBlog

A full-fledged blog application build using flask. FlaskBlog is a comprehensive blog application developed using Flask, a micro web framework in Python. This README provides a step-by-step guide to setting up, configuring, and using FlaskBlog.

#### Generating a Secret Key in `__init__.py` File:

1. Open the terminal:
2. Enter the Python interactive shell:

   ```bash
   $ python
   ```

3. Generate a secret key using the secrets module:

   ```bash
   >>> import secrets
   >>> secrets.token_hex(16)
   ```

4. Copy the generated key and paste it in the `__init__.py` file in the place of "GENERATED_KEY"
   `app.config['SECRET_KEY'] = 'GENERATED_KEY'`

5. Save the file and run the application.

#### Setting Up and Using FlaskBlog using `flask_sqlalchemy`:

1. Navigate to the FlaskBlog directory in your terminal.
2. Launch the Python interactive shell:

   ```bash
   $ python
   ```

3. Then Run the below commands to Initialize the database and create tables:

   ```bash
   >>> from FlaskBlog import db, app
   >>> from FlaskBlog.models import User, Post
   >>> with app.app_context():
   ...   db.create_all()
   ...
   ```

4. Create a new user:

   ```bash
      >>> with app.app_context():
      ...   new_user = User(username='username', email='email', password='password')
      ...   db.session.add(new_user)
      ...   db.session.commit()
      ...
   ```

5. Retrieve all users to verify the user creation:

   ```bash
   >>> with app.app_context():
   ...   all_users = User.query.all()
   ...   print(all_users)
   ```

6. Create a new post:
   ```bash
   >>> with app.app_context():
   ...   new_post = Post(title='title', content='content', user_id=1)
   ...   db.session.add(new_post)
   ...   db.session.commit()
   ```

#### Encrypting and Verifying Passwords with Flask-Bcrypt:

```bash
$ python
```

```bash
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> password = 'password'
>>> hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
>>> hashed_password
>>> bcrypt.check_password_hash(hashed_password, password)
```

#### Generating Secure Time System Tokens:

```bash
$ python
```

1. Import Required Module:

   ```bash
   >>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
   ```

2. Initialize Serializer:

   ```bash
   >>> s = Serializer('secret', 30)
   ```

3. Generate Token:

   ```bash
   >>> token = s.dumps({'user_id': 1}).decode('utf-8')
   ```

4. Access Token:

   ```bash
   >>> token
   'eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxMzY0MTA4MSwiZXhwIjoxNzEzNjQxMTExfQ.eyJ1c2VyX2lkIjoxfQ.mIftgDnRcaCAfzp68k88QGO_i4ajWyqFGmbajLAm7p-ay3n8hxNTBZh1sbpXSe_lpMkLMsx74ybKOCKvOXjJpg'
   ```

5. Verify Token:

   ```bash
   >>> s.loads(token)   # Access within 30 seconds
   {'user_id': 1}
   ```
