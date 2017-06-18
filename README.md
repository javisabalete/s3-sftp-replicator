# s3-sftp-replicator
Replicate changes on AWS S3 bucket via SFTP. For every event (create/modify/delete), replicate action to SFTP server using [environment variables](http://docs.aws.amazon.com/lambda/latest/dg/env_variables.html)

## Usage

1. Clone repo

    ```bash
    git clone https://github.com/JaviSabalete/s3-sftp-replicator.git
    ```

2. Build and start containers.

    ```bash
    docker-compose up --build
    ```

On finish, your project will have been packaged in ```proj.zip```, ready to upload in aws lambda.

3. Create environment variables [environment variables](http://docs.aws.amazon.com/lambda/latest/dg/env_variables.html)

4. Upload ```proj.zip``` to aws lambda. [Read official docu](http://docs.aws.amazon.com/lambda/latest/dg/with-s3.html)

5. Test it

Pull request always are welcome
