#
# Conditional build:
%bcond_with	doc	# build docs (broken)
%if "%{pld_release}" == "ti"
%bcond_without java_sun        # build with gcj
%else
%bcond_with    java_sun        # build with java-sun
%endif

%include	/usr/lib/rpm/macros.java

%define		srcname	mx4j
Summary:	Open source implementation of JMX Java API
Summary(pl.UTF-8):	Implementacja API Javy JMX z otwartymi źródłami
Name:		java-mx4j
Version:	3.0.2
Release:	0.2
Epoch:		0
License:	Apache
Group:		Development/Languages/Java
Source0:	http://dl.sourceforge.net/mx4j/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	1c01f620c21efb0a84c3105c064b9047
Patch0:		java-mx4j-sourcetarget.patch
URL:		http://mx4j.sourceforge.net/
BuildRequires:	ant >= 1.7
BuildRequires:	ant-trax
# BuildRequires:	axis
BuildRequires:	jaf
BuildRequires:	jakarta-bcel >= 5.0
BuildRequires:	jakarta-commons-logging >= 1.0.1
BuildRequires:	javamail >= 1.2
BuildRequires:	java-gcj-compat-devel
%{!?with_java_sun:BuildRequires:        java-gcj-compat-devel}
#%%{!?with_java_sun:BuildRequires:        java-gnu-classpath}
%{?with_java_sun:BuildRequires: java-sun}
BuildRequires:	java-hessian
BuildRequires:	jce >= 1.2.2
BuildRequires:	jpackage-utils
BuildRequires:	jsse >= 1.0.2
BuildRequires:	rpm-javaprov
BuildRequires:	junit >= 3.8
BuildRequires:	jython >= 2.1
BuildRequires:	logging-log4j >= 1.2.7
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xml-commons
Provides:	jmxri
Obsoletes:	openjmx
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenJMX is an open source implementation of the Java(TM) Management
Extensions (JMX).

%description -l pl.UTF-8
OpenJMX to implementacja standardu JMX (Java(TM) Management
Extensions) z otwartymi źródłami.

%package doc
Summary:	Manual for %{name}
Summary(fr.UTF-8):	Documentation pour %{name}
Summary(it.UTF-8):	Documentazione di %{name}
Summary(pl.UTF-8):	Podręcznik dla %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l fr.UTF-8
Documentation pour %{name}.

%description doc -l it.UTF-8
Documentazione di %{name}.

%description doc -l pl.UTF-8
Dokumentacja do %{name}.

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc do %{name}.

%prep
%setup -q

%build
required_jars="\
axis \
activation \
mail \
jython \
commons-logging \
xml-commons-apis \
bcel \
jsse \
jce \
log4j \
junit \
jaxp_transform_impl \
tools \
ecj \
libgcj \
servlet \
hessian \
glibj
"

CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

#ln -sf %{_javalibdir}/commons-logging.jar lib/
#ln -sf %{_javalibdir}/mail.jar lib/
#ln -sf %{_javalibdir}/activation.jar lib/
#ln -sf %{_javalibdir}/jython.jar lib/
#ln -sf %{_javalibdir}/log4j.jar lib/
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-jmx-module.jar
#ln -sf xdoclet-cvs20021028-patched.jar lib/xdoclet-mx4j-module.jar

cd build
%ant main %{?with_docs:javadocs docs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/lib/%{srcname}-actions.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-actions-%{version}.jar
cp -a dist/lib/%{srcname}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-jmx-%{version}.jar
cp -a dist/lib/%{srcname}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tools-%{version}.jar
ln -sf %{srcname}-actions-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-actions.jar
ln -sf %{srcname}-jmx-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-jmx.jar
ln -sf %{srcname}-tools-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-tools.jar

# javadoc
%if %{with doc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%if %{with doc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
