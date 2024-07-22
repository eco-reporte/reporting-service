from flask import request, jsonify
from werkzeug.utils import secure_filename
from src.reports.application.services.report_service import ReportService

class ReportController:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    def create_report(self):
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No file part'}), 400

            image = request.files['image']
            if image.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            data = {
                'titulo_reporte': request.form.get('titulo_reporte'),
                'tipo_reporte': request.form.get('tipo_reporte'),
                'descripcion': request.form.get('descripcion'),
                'colonia': request.form.get('colonia'),
                'codigo_postal': request.form.get('codigo_postal'),
                'fecha_creacion': request.form.get('fecha_creacion'),
                'nombres': request.form.get('nombres'),
                'apellidos': request.form.get('apellidos'),
                'telefono': request.form.get('telefono'),
                'correo': request.form.get('correo')
            }

            report = self.report_service.create_report(data, image)
            return jsonify(report.to_dict()), 201
        except Exception as e:
            print(f"Error en create_report controller: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def get_all_reports(self):
        try:
            reports = self.report_service.get_all_reports()
            return jsonify([report.to_dict() for report in reports]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_report(self, report_id):
        try:
            report = self.report_service.get_report_by_id(report_id)
            if report:
                return jsonify(report.to_dict()), 200
            return jsonify({'error': 'Report not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update_report(self, report_id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No input data provided'}), 400
            report = self.report_service.update_report(report_id, data)
            if report:
                return jsonify(report.to_dict()), 200
            return jsonify({'error': 'Report not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def patch_report(self, report_id):
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No input data provided'}), 400
            report = self.report_service.update_report(report_id, data)
            if report:
                return jsonify(report.to_dict()), 200
            return jsonify({'error': 'Report not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_report(self, report_id):
        try:
            deleted = self.report_service.delete_report(report_id)
            if deleted:
                return jsonify({'message': 'Report deleted successfully'}), 200
            return jsonify({'error': 'Report not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_all_reports(self):
        try:
            result = self.report_service.delete_all_reports()
            return jsonify({
                'message': 'Successfully deleted all reports and associated files',
                'deleted_files': result['deleted_files'],
                'deleted_db_records': result['deleted_db_records']
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_pdf_list(self):
        try:
            pdf_list = self.report_service.get_pdf_list()
            return jsonify(pdf_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500