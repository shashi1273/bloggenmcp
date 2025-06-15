# AWS Deployment Guide for MCP Technical Blog Server

This comprehensive guide provides detailed instructions for deploying the MCP Technical Blog Server, including both its Flask backend API and React frontend, to your Amazon Web Services (AWS) account. By following these steps, you will be able to host your blog generation tool in a scalable, reliable, and secure cloud environment.

## Table of Contents

1.  **Introduction**
2.  **Prerequisites**
3.  **Backend Deployment (Flask API)**
    *   Setting up Elastic Beanstalk
    *   Configuring the Flask Application
    *   Deploying the Backend
4.  **Frontend Deployment (React Application)**
    *   Setting up S3 for Static Website Hosting
    *   Configuring CloudFront for Content Delivery
    *   Deploying the Frontend
5.  **Post-Deployment Configuration and Verification**
    *   Updating Frontend API Endpoint
    *   Testing the Deployed Application
6.  **Troubleshooting and Best Practices**
7.  **Conclusion**
8.  **References**




## 3. Backend Deployment (Flask API)

This section outlines the process of deploying the Flask backend API of your MCP Technical Blog Server to AWS Elastic Beanstalk. Elastic Beanstalk is an easy-to-use service for deploying and scaling web applications and services developed with Python, Java, .NET, Node.js, Ruby, PHP, Go, and Docker on familiar servers such as Apache, Nginx, Passenger, and IIS [1].

### 3.1. Setting up Elastic Beanstalk

To begin, you will need to set up an Elastic Beanstalk environment. This involves creating an application and an environment within Elastic Beanstalk, specifying the platform as Python.

1.  **Sign in to the AWS Management Console:** Navigate to the Elastic Beanstalk service.
2.  **Create a New Application:** Click on "Create Application" and provide a suitable name for your application, for example, `mcp-blog-server-backend`.
3.  **Create a New Environment:** Within your newly created application, click on "Create a new environment". Choose "Web server environment".
4.  **Select Platform:** For the platform, select "Python". Elastic Beanstalk will automatically suggest a recommended Python version (e.g., Python 3.8 running on Amazon Linux 2). Ensure this matches your development environment or is compatible.
5.  **Application Code:** For now, select "Sample application". We will upload our code later.
6.  **Configure Environment:** Click "Configure more options" to customize your environment settings. Here, you can adjust instance types, scaling policies, and network settings. For a basic deployment, the default settings are often sufficient, but consider the following:
    *   **Software:** Ensure the Python version is correct. You can also specify environment properties here, which are crucial for Flask applications.
    *   **Instances:** Choose an appropriate instance type (e.g., `t2.micro` for testing, `t2.medium` or `t2.large` for production). Configure scaling settings based on your expected traffic.
    *   **Network:** Configure your VPC, subnets, and security groups. Ensure that your security group allows inbound traffic on port 80 (HTTP) and potentially 443 (HTTPS) if you plan to use SSL/TLS.
7.  **Create Environment:** Review your settings and click "Create environment". Elastic Beanstalk will provision the necessary AWS resources (EC2 instances, load balancers, security groups, etc.), which may take several minutes.

### 3.2. Configuring the Flask Application for Elastic Beanstalk

Elastic Beanstalk expects your Flask application to be structured in a specific way. The primary entry point for your application should be named `application.py` or `wsgi.py`, and the Flask application instance within that file should be named `application`. If your main Flask application file is named `main.py` and your Flask app instance is named `app` (as in the provided `mcp-blog-api` project), you will need to make a small configuration change.

Create a file named `.ebextensions/01_app.config` in the root of your `mcp-blog-api` project directory with the following content:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: src/main.py
```

This configuration tells Elastic Beanstalk to look for your Flask application instance (`app`) within `src/main.py`. If your Flask application instance is named something other than `application`, you would also need to specify it, for example: `WSGIPath: src/main.py:app`.

Additionally, ensure your `requirements.txt` file is up-to-date and includes all necessary Python dependencies, including `flask-cors` and `gunicorn`. Gunicorn is a Python WSGI HTTP Server for UNIX, and it's commonly used in production deployments of Flask applications.

```bash
cd /home/ubuntu/mcp-blog-api
source venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

Your `requirements.txt` should now include `gunicorn`.

### 3.3. Deploying the Backend

Once your Elastic Beanstalk environment is ready and your Flask application is configured, you can deploy your backend code. This involves packaging your application and uploading it to Elastic Beanstalk.

1.  **Prepare your application for deployment:** Create a `.zip` file containing your entire `mcp-blog-api` project directory. Ensure that the `.zip` file contains all your source code, `requirements.txt`, and the `.ebextensions` directory at the root level.

    ```bash
    cd /home/ubuntu/mcp-blog-api
    zip -r ../mcp-blog-api-eb.zip .
    ```

    This command will create `mcp-blog-api-eb.zip` in the `/home/ubuntu` directory.

2.  **Upload and Deploy:**
    *   Go back to your Elastic Beanstalk environment in the AWS Management Console.
    *   Click on "Upload and Deploy".
    *   Choose the `mcp-blog-api-eb.zip` file you just created.
    *   Optionally, provide a version label and description.
    *   Click "Deploy".

Elastic Beanstalk will then deploy your application. You can monitor the deployment status in the environment's dashboard. Once the deployment is successful, you will see a green checkmark and the environment's health will be "Ok". The environment overview will also display the URL of your deployed backend API.

**Important Note on Environment Variables:** If your Flask application uses environment variables (e.g., for API keys or database connections), you should configure these within the Elastic Beanstalk environment settings under "Software" -> "Environment properties". Do not hardcode sensitive information directly into your application code.





## 4. Frontend Deployment (React Application)

This section details the process of deploying the React frontend of your MCP Technical Blog Server. For static website hosting, AWS S3 is an ideal choice, offering high availability and scalability. To further enhance performance and security, we will integrate AWS CloudFront, a content delivery network (CDN).

### 4.1. Setting up S3 for Static Website Hosting

Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance. It is perfect for hosting static websites.

1.  **Create an S3 Bucket:**
    *   Sign in to the AWS Management Console and navigate to the S3 service.
    *   Click "Create bucket".
    *   **Bucket name:** Choose a unique and descriptive name for your bucket (e.g., `mcp-blog-server-frontend`). This name will be part of your website URL.
    *   **AWS Region:** Select the AWS Region closest to your users for optimal performance.
    *   **Object Ownership:** Enable "ACLs enabled" and choose "Bucket owner preferred" to ensure proper permissions for static website hosting.
    *   **Block Public Access settings for this bucket:** **Uncheck** "Block all public access". This is crucial for static website hosting, as your website content needs to be publicly accessible. Acknowledge the warning.
    *   **Bucket Versioning:** You can leave this disabled for a simple static site, but consider enabling it for production environments to manage different versions of your files.
    *   **Tags:** (Optional) Add tags for organization and cost allocation.
    *   **Default encryption:** (Optional) You can enable S3-managed encryption (SSE-S3) for data at rest.
    *   Click "Create bucket".

2.  **Enable Static Website Hosting:**
    *   Once the bucket is created, navigate to its properties.
    *   Scroll down to the "Static website hosting" section and click "Edit".
    *   Select "Enable" static website hosting.
    *   **Index document:** Enter `index.html`.
    *   **Error document:** Enter `index.html` (or a custom error page like `error.html` if you create one).
    *   Click "Save changes".

3.  **Configure Bucket Policy:**
    *   Go to the "Permissions" tab of your S3 bucket.
    *   Under "Bucket policy", click "Edit".
    *   Add a bucket policy that grants public read access to your objects. Replace `your-bucket-name` with your actual bucket name:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": [
                    "arn:aws:s3:::your-bucket-name/*"
                ]
            }
        ]
    }
    ```
    *   Click "Save changes".

### 4.2. Configuring CloudFront for Content Delivery

AWS CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency, high transfer speeds, all within a developer-friendly environment. Using CloudFront with S3 provides several benefits, including improved performance, SSL/TLS encryption, and custom domain support.

1.  **Create a CloudFront Distribution:**
    *   Navigate to the CloudFront service in the AWS Management Console.
    *   Click "Create distribution".
    *   **Origin domain:** Select your S3 bucket from the dropdown list. CloudFront will automatically suggest the S3 website endpoint (e.g., `your-bucket-name.s3-website.your-region.amazonaws.com`).
    *   **S3 bucket access:** Select "Yes, use OAI (Origin Access Identity)" to restrict direct S3 access and force users through CloudFront. This enhances security. Create a new OAI if you don't have one.
    *   **Viewer protocol policy:** Select "Redirect HTTP to HTTPS" to ensure all traffic uses secure HTTPS.
    *   **Allowed HTTP methods:** Select `GET, HEAD, OPTIONS` for static content.
    *   **Cache policy:** Use the "CachingOptimized" policy for general static content.
    *   **Price class:** Choose a price class based on your geographic distribution needs (e.g., "Use all edge locations (best performance)" for global reach).
    *   **Alternate domain names (CNAMEs):** (Optional) If you have a custom domain (e.g., `blog.yourdomain.com`), enter it here. You will need to configure a CNAME record in your DNS provider to point to your CloudFront distribution domain name.
    *   **SSL certificate:** (Optional) If using a custom domain, select a custom SSL certificate from AWS Certificate Manager (ACM). If you don't have one, you can request a new one through ACM.
    *   **Default root object:** Enter `index.html`.
    *   Click "Create distribution".

    The creation of the CloudFront distribution can take some time (10-20 minutes) as it propagates to all edge locations.

### 4.3. Deploying the Frontend

Once your S3 bucket and CloudFront distribution are set up, you can upload your React application's build files to the S3 bucket.

1.  **Build your React application for production:**

    ```bash
    cd /home/ubuntu/mcp-blog-frontend
    pnpm run build
    ```

    This command will create a `dist` (or `build`) directory containing the optimized static files for your React application.

2.  **Upload build files to S3:**
    *   Navigate to your S3 bucket in the AWS Management Console.
    *   Click on the "Upload" button.
    *   Drag and drop all the files and folders from your React application's `dist` directory into the S3 upload area.
    *   Ensure that all files are set to be publicly readable (this should be handled by your bucket policy, but double-check during upload if prompted).
    *   Click "Upload".

3.  **Invalidate CloudFront Cache (if necessary):**
    *   After uploading new files to S3, if you are using CloudFront, you might need to invalidate its cache to ensure that users receive the latest version of your website.
    *   Go to your CloudFront distribution in the AWS Management Console.
    *   Navigate to the "Invalidations" tab.
    *   Click "Create invalidation".
    *   For "Object paths", enter `/*` to invalidate all files (or specify individual file paths if you only updated a few).
    *   Click "Create invalidation".

Your React frontend will now be accessible via the CloudFront distribution domain name (e.g., `d12345abcdef.cloudfront.net`) or your custom domain if configured. Remember to update the frontend's API endpoint to point to your deployed Flask backend API URL.




## 5. Post-Deployment Configuration and Verification

After successfully deploying both the backend Flask API and the React frontend, it is crucial to perform post-deployment configurations and thorough verification to ensure that the entire application functions as expected.

### 5.1. Updating Frontend API Endpoint

Your React frontend application, once deployed, needs to know the exact URL of your deployed Flask backend API. During development, you might have used `http://localhost:5001` or a similar local address. Now, you must update this to the public URL provided by AWS Elastic Beanstalk after your backend deployment.

1.  **Retrieve Backend API URL:**
    *   Navigate to your Elastic Beanstalk environment in the AWS Management Console.
    *   On the environment dashboard, you will find the "Environment URL" (e.g., `http://mcp-blog-server-env.us-east-1.elasticbeanstalk.com`). This is the base URL for your backend API.

2.  **Update Frontend Code:**
    *   Locate the `src/App.jsx` file in your `mcp-blog-frontend` project. This is where the API calls are made.
    *   Find the `fetch` calls or any other API client configurations.
    *   Replace the placeholder or local backend URL with your actual Elastic Beanstalk environment URL. For example, if your backend URL is `http://mcp-blog-server-env.us-east-1.elasticbeanstalk.com`, your fetch call might look like this:

    ```javascript
    const response = await fetch("http://mcp-blog-server-env.us-east-1.elasticbeanstalk.com/api/generate-complete", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            topic: formData.topic,
            target_audience: formData.audience,
            keywords: formData.keywords,
            desired_length: formData.length
        })
    });
    ```

    **Important:** If you have configured HTTPS for your Elastic Beanstalk environment (which is highly recommended for production), ensure you use `https://` in your frontend code.

3.  **Rebuild and Redeploy Frontend:**
    *   After updating the API endpoint in your frontend code, you must rebuild your React application for production:

    ```bash
    cd /home/ubuntu/mcp-blog-frontend
    pnpm run build
    ```

    *   Then, upload the newly built files from the `dist` (or `build`) directory to your S3 bucket, overwriting the old files. Remember to invalidate your CloudFront cache if you are using CloudFront.

### 5.2. Testing the Deployed Application

Once both the backend and frontend are deployed and configured, it's time to thoroughly test the entire application to ensure all components are communicating correctly and functioning as expected.

1.  **Access the Frontend:** Open your deployed frontend website in a web browser using its CloudFront URL (e.g., `https://d12345abcdef.cloudfront.net`) or your custom domain.

2.  **Test Blog Generation:**
    *   Navigate to the "Blog Generator" tab.
    *   Enter a topic (e.g., "Quantum Computing"), select a target audience, provide some keywords (e.g., "qubits, entanglement, superposition"), and choose a content length.
    *   Click the "Generate Blog Post" button.
    *   Observe the "Generated Content" section. A successful generation will display the blog post title, introduction, and other details. If there are any errors, check the browser's developer console for network errors or API response issues.

3.  **Test Validation:**
    *   After generating a blog post, navigate to the "Validation" tab.
    *   Verify that the validation results are displayed correctly, showing any errors or warnings based on the business rules.

4.  **Test API Reference:**
    *   Go to the "API Reference" tab.
    *   Ensure that the API documentation (JSON schemas for `generate_complete_blog`, `validate_blog_post`, etc.) loads correctly. This confirms that the frontend can fetch the API reference from the backend.

5.  **Check Network Requests:** Use your browser's developer tools (usually F12) to inspect the network requests. Ensure that the frontend is making requests to your deployed backend API URL (e.g., `https://mcp-blog-server-env.us-east-1.elasticbeanstalk.com/api/generate-complete`) and that these requests are returning successful responses (HTTP 200 OK).

6.  **Monitor AWS Resources:** Keep an eye on your AWS CloudWatch logs for Elastic Beanstalk and CloudFront. These logs can provide valuable insights into any issues with your backend application or content delivery.





## 6. Troubleshooting and Best Practices

Deploying applications to the cloud can sometimes present challenges. This section provides common troubleshooting tips and best practices to ensure a smooth and efficient operation of your MCP Technical Blog Server on AWS.

### 6.1. Common Troubleshooting Scenarios

#### 6.1.1. Backend (Flask API) Issues

*   **502 Bad Gateway / 504 Gateway Timeout:**
    *   **Cause:** This often indicates that your Flask application is not running or is not accessible by the web server (Nginx/Apache) on the Elastic Beanstalk instance. It could be due to incorrect `WSGIPath`, missing dependencies, or application errors.
    *   **Solution:**
        *   **Check Elastic Beanstalk Logs:** Go to your Elastic Beanstalk environment, navigate to "Logs", and request the "Full logs". Look for errors in `web.stdout.log`, `web.stderr.log`, `/var/log/nginx/error.log`, or `/var/log/httpd/error_log`.
        *   **Verify `WSGIPath`:** Ensure that the `.ebextensions/01_app.config` file correctly points to your Flask application instance (e.g., `src/main.py:app`).
        *   **Check `requirements.txt`:** Confirm that all Python dependencies, including `gunicorn`, are listed in `requirements.txt` and are correctly installed. Missing dependencies are a common cause of deployment failures.
        *   **Application Errors:** If your application has unhandled exceptions, it might crash. Add robust error logging to your Flask app and check the logs.
        *   **Port Conflicts:** Ensure your Flask app is configured to run on a port that doesn't conflict with other services on the EC2 instance (Elastic Beanstalk typically handles this, but it's worth checking if you've customized the server).

*   **"No module named 'application'" or similar import errors:**
    *   **Cause:** Elastic Beanstalk expects a file named `application.py` with an `application` object by default. If your main file or app instance has a different name, you need to explicitly tell Elastic Beanstalk where to find it.
    *   **Solution:** As mentioned in Section 3.2, use the `.ebextensions` configuration to specify the `WSGIPath` to your main Flask file and the application object (e.g., `src/main.py:app`).

*   **CORS Issues (Frontend cannot access Backend):**
    *   **Cause:** Your Flask backend is not configured to allow cross-origin requests from your frontend domain.
    *   **Solution:** Ensure `flask-cors` is installed and properly configured in your `src/main.py` (or equivalent) file, allowing requests from your frontend's domain. For development or testing, `CORS(app, origins="*")` can be used, but for production, it's best to specify your frontend's domain (e.g., `CORS(app, origins="https://your-frontend-domain.com")`).

#### 6.1.2. Frontend (React Application) Issues

*   **Blank Page or "Cannot GET /" Error:**
    *   **Cause:** The `index.html` file is not correctly configured as the index document in S3 static website hosting, or the build files are not uploaded to the correct location.
    *   **Solution:**
        *   **Verify S3 Static Website Hosting:** Double-check that static website hosting is enabled for your S3 bucket and that `index.html` is specified as both the index and error document.
        *   **Check S3 Upload Path:** Ensure that the contents of your React `dist` (or `build`) folder are uploaded directly to the root of your S3 bucket, not into a subfolder.
        *   **Public Access:** Confirm that your S3 bucket policy grants public read access to all objects.

*   **Content Not Updating After Deployment:**
    *   **Cause:** CloudFront is serving cached content, or your browser has cached the old version.
    *   **Solution:**
        *   **Invalidate CloudFront Cache:** Perform a CloudFront invalidation for `/*` after every new frontend deployment to ensure the latest content is served.
        *   **Hard Refresh Browser:** Clear your browser's cache and perform a hard refresh (Ctrl+F5 or Cmd+Shift+R) to ensure you're not seeing a cached version.

*   **Frontend Cannot Connect to Backend API:**
    *   **Cause:** Incorrect backend API URL in the frontend code, or backend API is not running/accessible.
    *   **Solution:**
        *   **Verify Backend URL:** Ensure the backend API URL in your frontend's `src/App.jsx` (or equivalent) is correct and points to your deployed Elastic Beanstalk environment URL.
        *   **Check Backend Status:** Confirm that your Elastic Beanstalk environment is healthy and the Flask application is running. Check Elastic Beanstalk logs for any backend errors.
        *   **Security Group:** Ensure the security group associated with your Elastic Beanstalk EC2 instances allows inbound traffic on the port your Flask app is listening on (usually 80 or 443 if using HTTPS).

### 6.2. Best Practices for AWS Deployment

*   **Use Version Control:** Always use Git for your project and maintain a clean history. This helps in tracking changes and rolling back if necessary.
*   **Automate Deployments:** For continuous integration/continuous deployment (CI/CD), consider using AWS CodePipeline, CodeBuild, or GitHub Actions to automate your deployment process. This reduces manual errors and speeds up releases.
*   **Monitor Your Application:** Utilize AWS CloudWatch to monitor the health, performance, and logs of your Elastic Beanstalk environment and CloudFront distribution. Set up alarms for critical metrics.
*   **Implement HTTPS:** Always use HTTPS for both your frontend and backend. For Elastic Beanstalk, you can configure an SSL certificate on the load balancer. For CloudFront, you can use AWS Certificate Manager (ACM) to provision and manage SSL certificates.
*   **Security Groups and IAM Roles:** Configure AWS Security Groups to restrict inbound and outbound traffic to only what is necessary. Use IAM roles with the principle of least privilege for all AWS services and resources.
*   **Environment Variables:** Store sensitive information (API keys, database credentials) as environment variables in Elastic Beanstalk rather than hardcoding them in your application code.
*   **Cost Optimization:** Monitor your AWS costs regularly. Use appropriate instance types, scale down resources during low traffic periods, and consider Reserved Instances or Savings Plans for long-term cost savings.
*   **Backup and Recovery:** Implement a backup strategy for your data (e.g., S3 bucket contents, database backups). Understand AWS disaster recovery options.
*   **Logging and Tracing:** Implement comprehensive logging within your application. Consider using AWS X-Ray for distributed tracing to understand the performance of your application across different services.
*   **CDN for Frontend:** Always use a CDN like CloudFront for your static frontend assets. This improves performance by caching content closer to your users and reduces the load on your S3 bucket.

By adhering to these best practices and being prepared for common troubleshooting scenarios, you can ensure a robust, scalable, and secure deployment of your MCP Technical Blog Server on AWS.




## 1. Introduction

Welcome to the comprehensive guide for deploying your Model Context Protocol (MCP) Technical Blog Server on Amazon Web Services (AWS). This document will walk you through the essential steps to host both the Flask backend API and the React frontend application in a robust, scalable, and secure cloud environment. Leveraging AWS services such as Elastic Beanstalk for the backend and S3 with CloudFront for the frontend, you will establish a production-ready infrastructure for your AI-powered technical content generation tool.

This guide is designed for developers and system administrators who have a basic understanding of AWS concepts and command-line operations. By the end of this guide, you will have a fully functional MCP Technical Blog Server accessible globally, capable of generating high-quality technical blogs with integrated business rule validation.

## 2. Prerequisites

Before you begin the deployment process, ensure you have the following prerequisites in place:

*   **AWS Account:** An active AWS account with appropriate permissions to create and manage services like EC2, S3, CloudFront, Elastic Beanstalk, IAM, and Route 53.
*   **AWS CLI:** The AWS Command Line Interface (CLI) installed and configured on your local machine. Ensure you have configured your AWS credentials.
*   **Python and Pip:** Python 3.x and pip installed on your local machine for managing backend dependencies.
*   **Node.js and pnpm:** Node.js (LTS version recommended) and pnpm installed on your local machine for managing frontend dependencies and building the React application.
*   **Git:** Git installed for version control.
*   **MCP Technical Blog Server Codebase:** You should have the complete codebase for both the `mcp-blog-api` (Flask backend) and `mcp-blog-frontend` (React frontend) projects. This includes the `server.py`, `blog_generator.py`, `requirements.txt` for the backend, and the `src` directory, `package.json` for the frontend.
*   **Basic Understanding of AWS:** Familiarity with core AWS services like EC2, S3, and general cloud concepts will be beneficial.
*   **Domain Name (Optional but Recommended):** A registered domain name if you wish to use a custom URL for your website (e.g., `blog.yourcompany.com`).





## 7. Conclusion

Congratulations! You have successfully deployed the MCP Technical Blog Server, encompassing both its Flask backend API and React frontend, to your AWS account. By following this comprehensive guide, you have leveraged powerful AWS services like Elastic Beanstalk, S3, and CloudFront to create a robust, scalable, and highly available platform for generating technical blog content. This deployment provides a solid foundation for your AI-powered content creation needs, enabling you to manage and scale your operations efficiently in the cloud.

Remember to continuously monitor your AWS resources, implement security best practices, and keep your application dependencies updated to ensure optimal performance and security. With your MCP Technical Blog Server now live on AWS, you are well-equipped to streamline your technical content generation process and deliver high-quality articles to your audience.

## 8. References

[1] AWS Elastic Beanstalk Documentation. *Deploying a Flask application to Elastic Beanstalk*. Available at: [https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
[2] AWS Amplify Documentation. *Task 1: Deploy and Host a React App*. Available at: [https://aws.amazon.com/getting-started/hands-on/build-react-app-amplify-graphql/module-one/](https://aws.amazon.com/getting-started/hands-on/build-react-app-amplify-graphql/module-one/)
[3] Amazon S3 Documentation. *Hosting a static website using Amazon S3*. Available at: [https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
[4] AWS CloudFront Documentation. *Getting started with CloudFront*. Available at: [https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html)


