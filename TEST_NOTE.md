    def test_resend_User_otp_bad_request(self):
        data = {"email": "abram@hello.com"}
        response = self.client.post(
            "http://127.0.0.1:8000/rest_routes/resend_otp_code/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"status": "failed", "message": "Credentials does not match our record!"},
        )

    def test_confirm_otp_bad_request(self):
        data = {"email": "abram@test.com", "otp_code": "453521"}
        response = self.client.post(
            "http://127.0.0.1:8000/rest_routes/confirm_otp/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        response = self.client.post("http://127.0.0.1:8000/rest_routes/logout/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_email_otp_verify_page(self):
        response = self.client.get("http://127.0.0.1:8000/rest_routes/otp_verify/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emails/authentication/otp_verify.html")

    def test_welcome_user_page(self):
        response = self.client.get("http://127.0.0.1:8000/rest_routes/welcome/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emails/users/welcome.html")    def test_resend_User_otp_bad_request(self):
        data = {"email": "abram@hello.com"}
        response = self.client.post(
            "http://127.0.0.1:8000/rest_routes/resend_otp_code/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"status": "failed", "message": "Credentials does not match our record!"},
        )

    def test_confirm_otp_bad_request(self):
        data = {"email": "abram@test.com", "otp_code": "453521"}
        response = self.client.post(
            "http://127.0.0.1:8000/rest_routes/confirm_otp/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        response = self.client.post("http://127.0.0.1:8000/rest_routes/logout/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_email_otp_verify_page(self):
        response = self.client.get("http://127.0.0.1:8000/rest_routes/otp_verify/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emails/authentication/otp_verify.html")

    def test_welcome_user_page(self):
        response = self.client.get("http://127.0.0.1:8000/rest_routes/welcome/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emails/users/welcome.html")