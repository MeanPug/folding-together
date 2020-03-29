{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "frontend-registration-payments.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "frontend-registration-payments.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "frontend-registration-payments.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "frontend-registration-payments.labels" -}}
app.kubernetes.io/name: {{ include "frontend-registration-payments.name" . }}
helm.sh/chart: {{ include "frontend-registration-payments.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Common env
*/}}
{{- define "frontend-registration-payments.env" -}}
- name: DB_HOST
  value: {{ include "frontend-registration-payments.name" . }}-postgresql
- name: DB_USER
  value: "{{ .Values.postgresql.postgresqlUsername }}"
- name: DB_NAME
  value: "{{ .Values.postgresql.postgresqlDatabase }}"
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: frontend-registration-postgres-creds
      key: postgresql-password
- name: STATIC_ROOT
  value: /var/www/html/static
- name: AWS_DEFAULT_REGION
  value: us-east-1
- name: AWS_SQS_DONATION_QUEUE
  value: {{ .Values.application.env.aws_sqs_donation_queue }}
- name: STRIPE_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: stripe-keys
      key: secret_key
{{- end -}}
