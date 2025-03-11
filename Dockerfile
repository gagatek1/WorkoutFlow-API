FROM python:3.12

ENV HOME /home/appuser

RUN apt-get update -qq && apt-get install -y nodejs postgresql-client
RUN mkdir $HOME
RUN groupadd -g 1000 appuser && useradd -r -u 1000 -g appuser -d $HOME appuser

RUN mkdir $HOME/crewcontrol_api
WORKDIR $HOME/crewcontrol_api
RUN chown appuser:appuser -R $HOME
RUN chmod -R 775 $HOME

COPY requirements.txt ./
COPY . ./

RUN mkdir -p $HOME/crewcontrol_api/tmp/uploads/cache

RUN chown appuser:appuser -R $HOME

USER appuser

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN

ENV PATH /home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]