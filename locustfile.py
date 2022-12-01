from locust import HttpUser, task


class WebsiteUser(HttpUser):

    @task
    def prime_number(self):
        self.client.get(url=f"/prime/17")

    @task
    def invert_colors(self):
        image = open("test_image.jpg", "rb")
        image_data = image.read()
        self.client.post(url="/picture/invert", files={"file": image_data})

    @task
    def get_time(self):
        self.client.get(url="/time", auth=("admin", "admin"))
