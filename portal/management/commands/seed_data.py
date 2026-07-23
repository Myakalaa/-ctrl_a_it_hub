from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import Course, Service, Testimonial, HeroBanner, StudentProfile

class Command(BaseCommand):
    help = 'Seeds initial courses, services, testimonials, banners, and default admin user.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 1. Create Default Admin User
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@ctrlaithub.com', 'admin123')
            admin_user.first_name = 'CTRL A'
            admin_user.last_name = 'Admin'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created: username=admin, password=admin123'))

        # 2. Seed Hero Banners
        if HeroBanner.objects.count() == 0:
            HeroBanner.objects.create(
                title="Empowering Technologies & People",
                subtitle="CTRL A IT HUB is a professional training and IT services organization focused on skill development, internships, placements, and software solutions.",
                image="banners/banner1.png",
                is_active=True,
                display_order=1
            )
            HeroBanner.objects.create(
                title="Industrial Internship & Assured Placements",
                subtitle="Join our full stack programs in Java and Python to work on live APIs, database architectures, and clear placement screening rounds.",
                image="banners/banner2.png",
                is_active=True,
                display_order=2
            )
            self.stdout.write(self.style.SUCCESS('Default Hero Banners created.'))

        # 3. Seed Services
        if Service.objects.count() == 0:
            # IT / Academic Projects
            Service.objects.create(category='it_consulting', title='IT Consulting & Support', description='Software development consulting, code auditing, and business automation software architectures.')
            Service.objects.create(category='it_consulting', title='Academic Final-Year Projects', description='Practical, verified guidance for engineering students building Full Stack, ML, and Web applications.')
            Service.objects.create(category='it_consulting', title='Digital Transformation', description='Transitioning manual legacy client systems to modern cloud workflows, REST APIs, and responsive frontends.')
            
            # BPO
            Service.objects.create(category='bpo_projects', title='Customer Support Solutions', description='24/7 multi-channel tech support, call desk routing, email troubleshooting, and client relationship desks.')
            Service.objects.create(category='bpo_projects', title='Data Processing Services', description='High-integrity text entry, data classification, list management, and document indexing.')
            Service.objects.create(category='bpo_projects', title='Back Office Operations', description='Billing assistance, CRM logging, invoice audits, and general administrative backend operations.')
            
            # CSR
            Service.objects.create(category='csr_training', title='Skill Development Initiatives', description='Partnering with corporate organizations to provide local communities with practical tech competencies.')
            Service.objects.create(category='csr_training', title='Youth Employability Training', description='Empowering under-resourced graduates with direct technical knowledge and career readiness skills.')
            
            # Government
            Service.objects.create(category='gov_projects', title='Digital Literacy Training', description='Delivering fundamental web skills, safe browsing tutorials, and MS Office courses in local districts.')
            Service.objects.create(category='gov_projects', title='Technical Training Support', description='Supporting vocational education missions to enhance employment opportunities in public sectors.')
            self.stdout.write(self.style.SUCCESS('Corporate Services seeded.'))

        # 4. Seed Courses
        if Course.objects.count() == 0:
            # 1. Microsoft Office
            Course.objects.create(
                category='professional',
                title='Microsoft Office',
                description='Master essential desktop applications including Word, PowerPoint, Access, and Outlook for business and office environments.',
                syllabus='MS Word documents\nMS PowerPoint slides\nMS Outlook emailing\nMS Access database fundamentals',
                image='courses/msoffice.png',
                duration='2 Months',
                price='Rs. 5,000',
                is_featured=True
            )
            # 2. Fullstock Web Development
            Course.objects.create(
                category='web_technologies',
                title='Fullstock Web Development (CC++, Java, .Net, Python)',
                description='Complete end-to-end full stack development training covering frontend styling, database engines, and backend frameworks including Java, .Net, and Python.',
                syllabus='C/C++ Foundation\nJava Full Stack & Spring Boot\n.Net Core Web API\nPython Django MVC\nReact & Angular Frontend UI',
                image='courses/web.png',
                duration='6 Months',
                price='Rs. 28,000',
                is_featured=True
            )
            # 3. Advanced Excel
            Course.objects.create(
                category='professional',
                title='Advanced Excel',
                description='Learn sophisticated formulas, data filtering, lookups, pivot tables, and analytical macros for premium corporate tasks.',
                syllabus='VLOOKUP & HLOOKUP formulas\nPivot Tables & Pivot Charts\nData Validation & Sorting\nIntroduction to VBA & Macros',
                image='courses/excel.png',
                duration='1 Month',
                price='Rs. 6,000',
                is_featured=False
            )
            # 4. Digital Marketing
            Course.objects.create(
                category='web_technologies',
                title='Digital Marketing',
                description='Master SEO optimization, Google Adwords, Facebook ads, social media engagement campaigns, and web traffic analytics.',
                syllabus='Search Engine Optimization (SEO)\nSearch Engine Marketing (SEM)\nSocial Media Marketing (SMM)\nGoogle Analytics reports',
                image='courses/digitalmarketing.png',
                duration='3 Months',
                price='Rs. 10,000',
                is_featured=False
            )
            # Java Full Stack Development
            Course.objects.create(
                category='programming',
                title='Java Full Stack Development',
                description='Master Core Java, Advanced Java, Spring Boot microservices, Hibernate ORM, React frontend, and relational SQL database modeling.',
                syllabus='Core Java basics\nOOP Concepts\nCollections Framework\nAdvanced JDBC & Servlets\nSpring Boot REST APIs\nReact JS integration\nProject deployment',
                image='courses/java.png',
                duration='6 Months',
                price='Rs. 25,000',
                is_featured=True
            )
            # 5. Core Python & Advanced Python
            Course.objects.create(
                category='programming',
                title='Core Python & Advanced Python',
                description='Master Python syntax, object-oriented concepts, multithreading, API integrations, files handling, and script automation.',
                syllabus='Python basics & scripts\nOOP & Exception handling\nDatabase adapters & migrations\nMulti-threading & API structures',
                image='courses/python.png',
                duration='3 Months',
                price='Rs. 12,000',
                is_featured=True
            )
            # 6. Data Science (ML, Big Data, Tableau)
            Course.objects.create(
                category='testing_analytics',
                title='Data Science (ML, Big Data, Tensorflow, Pandas, Numpys, Tableau)',
                description='Learn advanced data collection, model building, neural networks, tabular analysis, and interactive dashboard visuals.',
                syllabus='Python NumPy & Pandas\nMachine Learning models\nTensorflow Neural Nets\nTableau visualizations\nBig Data pipelines',
                image='courses/datascience.png',
                duration='4 Months',
                price='Rs. 25,000',
                is_featured=True
            )
            # 7. Accounting Packages (Tally, GST)
            Course.objects.create(
                category='database_sap',
                title='Accounting Packages (Tally, GST)',
                description='Master Tally Prime bookkeeping, inventory auditing, payroll calculations, and local GST compliance reporting.',
                syllabus='Tally Prime bookkeeping\nGST transactions & reporting\nInventory auditing records\nPayroll setup calculations',
                image='courses/tally.png',
                duration='2 Months',
                price='Rs. 8,000',
                is_featured=False
            )
            # 8. AWS Devops, AZURE Devops, GCP Devops
            Course.objects.create(
                category='database_sap',
                title='AWS Devops, AZURE Devops, GCP Devops',
                description='Learn cloud continuous delivery, deployment automation, containerization with Docker, Kubernetes, and cloud configs.',
                syllabus='Cloud foundation (AWS, Azure, GCP)\nContinuous Integration & Deployments\nDocker & Kubernetes containers\nInfrastructure as Code (Terraform)',
                image='courses/devops.png',
                duration='4 Months',
                price='Rs. 20,000',
                is_featured=False
            )
            # 9. SAP Modules
            Course.objects.create(
                category='database_sap',
                title='SAP Modules',
                description='Learn SAP business modules, configuration screens, material management, financial accounting, and transaction codes.',
                syllabus='Introduction to SAP ERP\nSAP Material Management (MM)\nSAP Financial Accounting (FI)\nSAP Transaction Codes',
                image='courses/sap.png',
                duration='3 Months',
                price='Rs. 18,000',
                is_featured=False
            )
            # 10. Testing Tools (Automation...)
            Course.objects.create(
                category='testing_analytics',
                title='Testing Tools (Automation & Manual)',
                description='Master manual quality audits, writing test scenarios, Selenium Web Driver automation scripting, test execution, and CI/CD integrations.',
                syllabus='Manual QA test plans\nSelenium Automation with Java/Python\nTestNG & JUnit architectures\nJenkins & Git pipelines',
                image='courses/testing.png',
                duration='3 Months',
                price='Rs. 15,000',
                is_featured=True
            )
            # 11. Generative Artificial Intelligence (AI, AIML, Prompt Engg.)
            Course.objects.create(
                category='programming',
                title='Generative Artificial Intelligence (AI, AIML, Prompt Engg.)',
                description='Learn Prompt Engineering, Large Language Models, Generative Adversarial Networks, AI agent workflows, and vector stores.',
                syllabus='Intro to LLMs & Transformers\nPrompt Engineering techniques\nAI Model tuning APIs\nVector databases (Chroma, Pinecone)',
                image='courses/generativeai.png',
                duration='3 Months',
                price='Rs. 16,000',
                is_featured=True
            )
            # 12. Data Analytics (B.A.F.A & Statistics)
            Course.objects.create(
                category='testing_analytics',
                title='Data Analytics (B.A.F.A & Statistics)',
                description='Master statistical modeling, predictive trends, business intelligence, query scripts, and tabular cleanups.',
                syllabus='Business Statistics\nData collection & cleanups\nPredictive Analytics\nBusiness Intelligence reporting',
                image='courses/dataanalytics.png',
                duration='3 Months',
                price='Rs. 15,000',
                is_featured=False
            )
            # 13. Investment Banking & Globe Accounting
            Course.objects.create(
                category='database_sap',
                title='Investment Banking & Globe Accounting',
                description='Learn global financial systems, equity capital deals, portfolio management risk, and corporate bookkeeping.',
                syllabus='Global Financial Markets\nEquity Valuation & Assets\nPortfolio Risk management\nCorporate Bookkeeping audits',
                image='courses/investmentbanking.png',
                duration='3 Months',
                price='Rs. 22,000',
                is_featured=False
            )

            # Extra legacy courses (optional but kept for reference compatibility)
            Course.objects.create(
                category='programming',
                title='C / C++ Programming',
                description='Build solid foundational logic. Learn pointers, memory allocation, structures, file handling, and OOP design constructs in C++.',
                syllabus='Control structures\nFunctions & Pointers\nDynamic Memory\nClasses & Objects\nInheritance & Polymorphism\nFile streams',
                image='courses/cpp.png',
                duration='2 Months',
                price='Rs. 8,000',
                is_featured=False
            )
            Course.objects.create(
                category='database_sap',
                title='SQL & Oracle Database Management',
                description='Master data queries, writing stored procedures, triggers, indexing strategies, and database server schema designs.',
                syllabus='SQL fundamentals\nJoins & Subqueries\nDDL & DML scripts\nOracle PL/SQL blocks\nStored procedures & Triggers\nDatabase Performance Tuning',
                image='courses/sql.png',
                duration='3 Months',
                price='Rs. 12,000',
                is_featured=False
            )
            Course.objects.create(
                category='testing_analytics',
                title='Data Analytics with Power BI',
                description='Import, transform, and model data. Build interactive reports, calculations, and KPI tracking dashboards.',
                syllabus='Data collection & Cleanups\nPower Query transformations\nDAX calculations\nInteractive report designs\nPower BI Cloud service',
                image='courses/powerbi.png',
                duration='3 Months',
                price='Rs. 16,000',
                is_featured=False
            )
            Course.objects.create(
                category='professional',
                title='Soft Skills & Interview Preparation',
                description='Develop business English competency, resume summaries, body language, presentation habits, and clear HR interview answers.',
                syllabus='Effective communication\nResume formatting & audits\nGroup Discussion drills\nHR mock interviews\nCorporate work ethics',
                image='courses/softskills.png',
                duration='1 Month',
                price='Rs. 5,000',
                is_featured=False
            )
            self.stdout.write(self.style.SUCCESS('Courses seeded.'))

        # 5. Seed Testimonials
        if Testimonial.objects.count() == 0:
            Testimonial.objects.create(
                student_name='Amith Gowda',
                course_name='Java Full Stack Internship',
                review='The training was absolutely industry-grade. The mock interview sessions and practical labs gave me the confidence to clear the technical coding round at a global multinational service corporation.',
                rating=5
            )
            Testimonial.objects.create(
                student_name='Divya S.',
                course_name='Software QA & Selenium Automation Testing',
                review='I shifted from a non-IT background. The trainers explained manual and automation testing with extreme patience. The certificate and placement assistance helped me land a QA job quickly!',
                rating=5
            )
            self.stdout.write(self.style.SUCCESS('Testimonials seeded.'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
